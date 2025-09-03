from django.shortcuts import render # fungsi render dari modul django.shortcuts

# mengatur permintaan HTTP dan mengembalikan tampilan yang sesuai
def show_main(request):
    # dictionary data
    context = {
        'npm' : '2406346693',
        'name' : 'Waldan Rafid',
        'class' : 'PBP F'
    }
    # me-request render tampilan pada template "main.html" dengan data
    return render(request, "main.html", context)