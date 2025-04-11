from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from goods.models import Products


def search(query,category):
    # 1. Проверяем точное совпадение
    if category == 'all':
        exact_match = Products.objects.filter(name__iexact=query)
        if exact_match:
            return exact_match
    else:
        exact_match = Products.objects.filter(name__iexact=query,category__slug__iexact=category)
        if exact_match:
            return exact_match  # Если есть точное совпадение, возвращаем только его

    if query.isdigit() and len(query) <= 5:
        if category == 'all':
            return Products.objects.filter(id=int(query))
        else:
            return Products.objects.filter(category__slug=category, id=int(query))
    vector = SearchVector('name', 'description')
    # В Django SearchVector используется для полнотекстового поиска. Он превращает указанные поля в поисковый индекс, чтобы потом искать по ним.
    search_query = SearchQuery(query)
    # Преобразует переданный пользователем поисковый запрос (query) в объект SearchQuery, который можно сравнивать с SearchVector.
    if category == 'all':
        ranked_results = Products.objects.annotate(rank=SearchRank(vector, search_query)).filter(rank__gt=0).order_by('-rank')
        return ranked_results
    # annotate добавляет дополнительные поля в нашем случае поле rank которое указывает на сколько vector совпадает с search_query, filter фильтрует
    # и отсекает всё где rank меньше или равно нулю и затем сортируем по убыванию..filter(rank__gte=0.2) gte = "greater than or equal" (больше или равно)
    # а у нас только больше 0
    else:
        ranked_results = Products.objects.annotate(rank=SearchRank(vector, search_query)).filter(rank__gt=0,category__slug=category).order_by('-rank')
        return ranked_results

    # возможно этот поиск не нужен потому что у нас и так если совпадение не 0 то оно покажет это
    # 3. Если ничего не найдено — используем поиск по частичному совпадению (TrigramSimilarity) CREATE EXTENSION pg_trgm; чтобы это работало нужно ввести эту команду в sql
    # similar_results = Products.objects.annotate(
    #     similarity=TrigramSimilarity('name', query)).filter(similarity__gt=0.3,category__slug=category).order_by('-similarity')  # 0.4 — порог похожести (max 1)
    #
    # return similar_results
