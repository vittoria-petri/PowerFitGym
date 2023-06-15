from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .models import Esercizi, UserAssign, SchedaAssign, Scheda, ExUserAssign


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
        LSaveResult = str()
        LCBStatus = str()

        for i in range(0, len(L_Lista_Schede), 1):
            L_Lista_Esercizi = SchedaAssign.objects.filter(Scheda=L_Lista_Schede[i].Scheda)
            T_List.clear()

            for j in range(0, len(L_Lista_Esercizi), 1):
                if L_Lista_Esercizi[j].IsDone:
                    LCBStatus = "disabled Checked"
                else:
                    LCBStatus = ""
                T_Tuple = (L_Lista_Esercizi[j].Esercizio.name,
                           L_Lista_Esercizi[j].Esercizio.description,
                           L_Lista_Esercizi[j].Esercizio.get_category_display(),
                           L_Lista_Esercizi[j].Esercizio.ripetizioni,
                           L_Lista_Esercizi[j].Esercizio.carico,
                           L_Lista_Esercizi[j].Esercizio.ExID,
                           LCBStatus)
                T_List.append(T_Tuple)
            L_Lista[L_Lista_Schede[i].Scheda.NomeScheda] = list(T_List)

        if request.method == "POST":
            Lbreak = bool(False)
            LItemList = list(L_Lista.keys())
            LIndex = 0

            while LIndex < len(LItemList) and not Lbreak:
                if ("Submit" + str(LItemList[LIndex])) in request.POST:
                    Lbreak = True
                    LScheda = Scheda.objects.get(NomeScheda=LItemList[LIndex])
                    UserAssign.objects.get(Scheda=LScheda).delete()

                    if not LScheda.isDefault:
                        LOldScheda = Scheda.objects.get(Scheda=LScheda)
                        LExList = SchedaAssign.objects.filter(Scheda=LScheda)

                        for Item in LExList:
                            ExUserAssign.objects.get(ExRef=Item.Esercizio).delete()
                        LOldScheda.delete()
                    else:
                        LExList = SchedaAssign.objects.filter(Scheda=LScheda)

                        for Item in LExList:
                            if Item.IsDone:
                                Item.IsDone = False
                                Item.save()
                            ExUserAssign.objects.get(ExRef=Item.Esercizio).delete()
                    L_Lista.pop(LItemList[LIndex])
                elif ("exdone" + str(LItemList[LIndex])) in request.POST:
                    SchedaEs = Scheda.objects.get(NomeScheda=LItemList[LIndex])
                    LListaEsercizi = SchedaAssign.objects.filter(Scheda=SchedaEs)

                    for Item in LListaEsercizi:
                        if request.POST.get("n_exdone" + str(Item.Esercizio.ExID)):
                            LExUserRef = ExUserAssign.objects.get(UserRef=request.user, ExRef=Item.Esercizio)
                            LExUserRef.IsDone = True
                            LExUserRef.save()
                            Item.IsDone = True
                            Item.save()
                    LSaveResult = "Modifiche salvate!"
                    Lbreak = True
                    return redirect("/exercises/myworkout/")
                else:
                    LIndex += 1
        return render(request, "my_workout.html", {"Dict": L_Lista, "SaveResult": LSaveResult})
    else:
        return render(request, "my_workout.html")

def new_workout(request):
    LCreationResult = str()

    if request.method == "POST":
        if "Aggiungi" in request.POST:
            LNomeScheda = request.POST.get("n_nomescheda")
            LExList = list()
            LExFromTable = Esercizi.objects.all()
            LCount = len(Scheda.objects.filter(NomeScheda=LNomeScheda))
            LIndex = int(0)
            LBreak = bool(False)

            for Value in LExFromTable:
                LExList.append(Value.ExID)
            while LIndex < len(LExList) and not LBreak:
                if (request.POST.get("n_load" + str(LExList[LIndex])) == "" or request.POST.get(
                        "n_repetitions" + str(LExList[LIndex])) == "") and request.POST.get(
                        "n_selex" + str(LExList[LIndex])):
                    LBreak = True
                else:
                    LIndex += 1
            if LCount > 0:
                LCreationResult = "ATTENZIONE > Nome scheda già esistente"
            elif LBreak:
                LCreationResult = "ATTENZIONE > Uno o più esercizi selezionati hanno un campo numerico vuoto"
            elif LNomeScheda == "":
                LCreationResult = "ATTENZIONE > Inserisci un nome per la scheda"
            else:
                new_scheda = Scheda.objects.create(NomeScheda=LNomeScheda)
                new_scheda.save()
                user_assign = UserAssign.objects.create(User=request.user,
                                                        Scheda=Scheda.objects.get(NomeScheda=LNomeScheda))
                user_assign.save()

                for Value in LExList:
                    if request.POST.get("n_selex" + str(Value)):
                        LEsercizio = Esercizi.objects.get(ExID=Value)
                        LEsercizio.carico = request.POST.get("n_load" + str(Value))
                        LEsercizio.ripetizioni = request.POST.get("n_repetitions" + str(Value))
                        LEsercizio.save()
                        NewSchedaAssign = SchedaAssign.objects.create(Scheda=new_scheda, Esercizio=LEsercizio,
                                                                      Username=request.user.username)
                        NewSchedaAssign.save()
                        LExUserList = SchedaAssign.objects.filter(Esercizio=LEsercizio)

                        for Item in LExUserList:
                            NewExUserAssign = ExUserAssign.objects.create(UserRef=request.user, ExRef=Item.Esercizio)
                            NewExUserAssign.IsDone = False
                            NewExUserAssign.save()
                LCreationResult = "Scheda creata con successo"
        elif "Aggiungi2" in request.POST:
            l_select = request.POST.get("n_schedebase", "None")
            l_scheda = Scheda.objects.get(NomeScheda=l_select)
            LTempCount = len(UserAssign.objects.filter(User=request.user, Scheda=l_scheda))

            if LTempCount == 0:
                l_assign = UserAssign.objects.create(User=request.user, Scheda=l_scheda)
                l_assign.save()
                LAssignList = SchedaAssign.objects.filter(Scheda=l_scheda)

                for Item in LAssignList:
                    ExUserAssign.objects.create(UserRef=request.user, ExRef=Item.Esercizio).save()
                return redirect("/exercises/myworkout/")
            else:
                LCreationResult = "ATTENZIONE > Questa scheda esiste già nella tua lista"
    LFreeExList = Esercizi.objects.filter(isDefault=False)
    t_tuple = list(tuple(str()))
    for value in LFreeExList:
        t_tuple.append((value.get_category_display(), value.name, value.description, value.ExID))
    return render(request, "new_workout.html", {"lista_esercizi": t_tuple, "CreationResult": LCreationResult})


def ex_done(request):
    ListDone = list()
    LExUserList = ExUserAssign.objects.filter(UserRef=request.user)

    for Item in LExUserList:
        if Item.IsDone:
            ListDone.append(Item.ExRef.name)
    return render(request, "ex_done.html", {"ExDoneList": ListDone})
