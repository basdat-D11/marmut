from django.shortcuts import render

# Create your views here.
# View untuk menampilkan search bar
def search_bar(request):
    return render(request, 'search_bar.html')

# View untuk menampilkan hasil pencarian
def search_results(request):
    query = request.GET.get('query', '')
    context = {'query': query}  # Add 'query' to the context

    # Check if the query is not empty
    if query:

        if query.lower() == "love":
            data = [
                {'type': 'SONG', 'title': 'Love is in the air', 'by': 'Artist1'},
                {'type': 'SONG', 'title': 'What is love', 'by': 'Artist2'},
                {'type': 'PODCAST', 'title': 'Love is Blind Pod', 'by': 'Podcaster1'},
                {'type': 'USER PLAYLIST', 'title': '90s Love Songs', 'by': 'User1'},
            ]
            context['results'] = data
        else:
            pass

    return render(request, 'search_result.html', context)