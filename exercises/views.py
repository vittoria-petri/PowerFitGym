from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .models import Esercizi, UserAssign, SchedaAssign, Scheda


class EserciziListView(ListView):
    model = Esercizi
    template_name = "article_list.html"


class EserciziListViewUser(ListView):
    model = Esercizi
    template_name = "article_list.html"

    def get_queryset(self):
        return Esercizi.objects.all()

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)


class EserciziDetailView(DetailView):  # new
    model = Esercizi
    template_name = "article_detail.html"


class EserciziUpdateView(UpdateView):  # new
    model = Esercizi
    fields = ("category", "name", "description")
    template_name = "article_edit.html"


class EserciziDeleteView(DeleteView):  # new
    model = Esercizi
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")


class EserciziCreateView(CreateView):
    model = Esercizi
    template_name = "new_workout.html"
    fields = ("category", "name", "description")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            article = form.save(commit=False)
            article.author = self.request.user
            article.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def my_workout(request):
    if request.user.is_authenticated:
        L_User = request.user
        L_Lista_Schede = UserAssign.objects.filter(User=L_User)
        L_Lista = dict()
        T_List = list()

        for i in range(0, len(L_Lista_Schede), 1):
            L_Lista_Esercizi = SchedaAssign.objects.filter(Scheda=L_Lista_Schede[i].Scheda)
            T_List.clear()

            for j in range(0, len(L_Lista_Esercizi), 1):
                T_Tuple = (L_Lista_Esercizi[j].Esercizio.name, L_Lista_Esercizi[j].Esercizio.description,
                           L_Lista_Esercizi[j].Esercizio.get_category_display(),
                           L_Lista_Esercizi[j].Esercizio.ripetizioni,
                           L_Lista_Esercizi[j].Esercizio.get_carico_display())
                T_List.append(T_Tuple)
            L_Lista[L_Lista_Schede[i].Scheda.NomeScheda] = list(T_List)

        return render(request, "my_workout.html", {"Dict": L_Lista})
    else:
        return render(request, "my_workout.html")


def new_workout(request):
    if request.method == "POST":
        if "Aggiungi" in request.POST:
            LNomeScheda = request.POST["n_nomescheda"]
            LCount = len(Scheda.objects.filter(NomeScheda=LNomeScheda))

            if LCount > 0:
                return render(request, "new_workout.html", {"CreationResult": "Nome già esistente"})
            new_scheda = Scheda.objects.create(NomeScheda=LNomeScheda)
            new_scheda.save()
            user_assign = UserAssign.objects.create(User=request.user,
                                                    Scheda=Scheda.objects.get(NomeScheda=LNomeScheda))
            user_assign.save()
            list_esercizi = list()
            table_ex = Esercizi.objects.all()

            for Value in table_ex:
                list_esercizi.append(Value.ExID)
            for Value in list_esercizi:
                if request.POST.get("n_selex" + str(Value)):
                    LEsercizio = Esercizi.objects.get(ExID=Value)
                    NewSchedaAssign = SchedaAssign.objects.create(Scheda=new_scheda, Esercizio=LEsercizio)
                    NewSchedaAssign.save()
        return redirect("/exercises/myworkout/")
    else:
        l_list = Esercizi.objects.all()
        t_tuple = list(tuple(str()))
        for value in l_list:
            t_tuple.append((value.get_category_display(), value.name, value.description, value.ExID))
        print(l_list)
        return render(request, "new_workout.html", {"lista_esercizi": t_tuple})


def aggiungi_scheda(request):
    print("fewfififeyfy")

    if request.user.is_authenticated:
        if request.method == "POST":
            l_select = request.POST.get("n_schedebase", "None")
            l_scheda = Scheda.objects.filter(NomeScheda=l_select)
            l_assign = UserAssign.objects.create(User=request.user, Scheda=l_scheda)
            l_assign.save()
            return redirect("/exercises/myworkout/")
        return redirect("/")
    else:
        return render(request, "home.html")

