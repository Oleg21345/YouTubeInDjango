def author_context(request):
    autor = getattr(request.user, "autor", None)
    return {"autor": autor}