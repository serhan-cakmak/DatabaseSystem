from django.contrib import messages
from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
import mysql.connector
from datetime import datetime

from .utils.forms import *

load_dotenv()

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=os.environ.get("password"),
    database="volleydb",
    buffered=True
)


def home(request):
    print(request)
    if request.method == "POST":
        form = user_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            mycursor = mydb.cursor()
            mycursor.execute("select * from user u where u.username=%s and u.password=%s", (username, password)),
            myresult = mycursor.fetchone()
            mycursor.close()
            if myresult:
                for i in ["player", "coach", "jury"]:
                    mycursor = mydb.cursor()
                    mycursor.execute(f"select * from {i} u where u.username=%s", (username,))
                    myresult = mycursor.fetchone()
                    mycursor.close()
                    if myresult:
                        request.session["username"] = username
                        request.session["role"] = i
                        return redirect("dashboard")

                request.session["username"] = username
                request.session["role"] = "admin"
                return redirect("dashboard")

            else:
                form = user_form()
                context = {"form": form,
                           "message": "Invalid username or password"}

    else:
        form = user_form()
        context = {"form": form}

    return render(request, 'home.html', context)


def dashboard(request):
    if request.session.get("role") == "admin":
        if request.method == "POST":
            form = admin_form_select(request.POST)
            if form.is_valid():
                table = form.cleaned_data["table"]
                if table == "add":
                    return redirect("add")
                elif table == "update":
                    return redirect("update")
        else:
            form = admin_form_select()
            context = {"form": form}
            return render(request, 'dashboard.html', context)
    if request.session.get("role") == "coach":
        if request.method == "POST":
            form = coach_form_select(request.POST)
            if form.is_valid():
                table = form.cleaned_data["table"]
                if table == "delete_session":
                    return redirect("delete_session")
                elif table == "list_stadiums":
                    return redirect("list_stadiums")
                elif table == "add_match":
                    return redirect("add_match")


        else:
            form = coach_form_select()
            context = {"form": form}
            return render(request, 'dashboard.html', context)

    if request.session.get("role") == "jury":
        if request.method == "POST":
            form = jury_form_select(request.POST)
            if form.is_valid():
                table = form.cleaned_data["table"]
                if table == "get_info":
                    return redirect("get_info")
                elif table == "rate":
                    return redirect("rate")
        else:
            form = jury_form_select()
            context = {"form": form}
            return render(request, 'dashboard.html', context)
    # return render(request, 'dashboard.html')


def add(request):
    if request.method == "POST":
        form = admin_form_add(request.POST)
        if form.is_valid():
            table = form.cleaned_data["table"]
            if table == "player":
                return redirect("add_player")
            elif table == "coach":
                return redirect("add_coach")
            elif table == "jury":
                return redirect("add_jury")
    else:
        form = admin_form_add()
        context = {"form": form}
        return render(request, 'add.html', context)


def add_player(request):
    if request.method == "POST":
        form = add_player_form(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                name = form.cleaned_data["name"]
                surname = form.cleaned_data["surname"]
                date_of_birth = form.cleaned_data["date_of_birth"]
                height = form.cleaned_data["height"]
                weight = form.cleaned_data["weight"]
                mycursor = mydb.cursor()
                mycursor.execute("insert into user values(%s, %s, %s, %s)", (username, password, name, surname))
                mycursor.execute("insert into player values(%s, %s, %s, %s)", (username, date_of_birth, height, weight))
                mydb.commit()
                mycursor.close()
                messages.success(request, "User added successfully.")
                return redirect("add")
            except Exception as e:
                form = add_player_form()
                context = {"form": form}
                messages.error(request, "Username already exists")
                return render(request, 'add_player.html', context)

    else:
        form = add_player_form()
        context = {"form": form}
        return render(request, 'add_player.html', context)


def add_coach(request):
    if request.method == "POST":
        form = add_coach_form(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                name = form.cleaned_data["name"]
                surname = form.cleaned_data["surname"]
                nationality = form.cleaned_data["nationality"]
                mycursor = mydb.cursor()
                mycursor.execute("insert into user values(%s, %s, %s, %s)", (username, password, name, surname))
                mycursor.execute("insert into coach values(%s, %s)", (username, nationality))
                mydb.commit()
                mycursor.close()
                messages.success(request, "User added successfully.")
                return redirect("add")
            except Exception as e:
                form = add_coach_form()
                context = {"form": form}
                messages.error(request, "Username already exists")
                return render(request, 'add_coach.html', context)


    else:
        form = add_coach_form()
        context = {"form": form}
        return render(request, 'add_coach.html', context)


def add_jury(request):
    if request.method == "POST":
        form = add_coach_form(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                name = form.cleaned_data["name"]
                surname = form.cleaned_data["surname"]
                nationality = form.cleaned_data["nationality"]
                mycursor = mydb.cursor()
                mycursor.execute("insert into user values(%s, %s, %s, %s)", (username, password, name, surname))
                mycursor.execute("insert into jury values(%s, %s)", (username, nationality))
                mydb.commit()
                mycursor.close()
                messages.success(request, "User added successfully.")
                return redirect("add")
            except Exception as e:
                print(e)
                form = add_coach_form()
                context = {"form": form}
                messages.error(request, "Username already exists")

                return render(request, 'add_jury.html', context)
    else:
        form = add_jury_form()
        context = {"form": form}
        return render(request, 'add_jury.html', context)


def update(request):
    if request.method == "POST":
        form = update_stadium_form(request.POST)
        if form.is_valid():
            old_stadium_name = form.cleaned_data["old_stadium_name"]
            new_stadium_name = form.cleaned_data["new_stadium_name"]

            mycursor = mydb.cursor()
            mycursor.execute("select * from stadium s where s.stadium_name=%s", (old_stadium_name,))
            if mycursor.fetchone() is None:
                form = update_stadium_form()
                context = {"form": form}
                messages.error(request, "Stadium does not exist")
                return render(request, 'update_stadium.html', context)
            mydb.commit()
            mycursor.close()

            mycursor = mydb.cursor()
            mycursor.execute("update stadium set stadium_name=%s where stadium_name=%s",
                             (new_stadium_name, old_stadium_name))
            mydb.commit()
            mycursor.close()
            messages.success(request, "Stadium updated successfully")
            return redirect("dashboard")

    else:
        form = update_stadium_form()
        context = {"form": form}
        return render(request, 'update_stadium.html', context)


def delete_session(request):
    if request.method == "POST":
        form = delete_session_form(request.POST)
        if form.is_valid():
            try:
                session_id = form.cleaned_data["session_id"]
                mycursor = mydb.cursor()
                mycursor.execute("delete from sessionsquads s where s.session_ID=%s", (session_id,))
                mycursor.execute("delete from matchsession m where m.session_ID=%s", (session_id,))
                mydb.commit()
                mycursor.close()
                messages.success(request, "Session deleted successfully")
                return redirect("dashboard")

            except Exception as e:
                print(e)
                form = delete_session_form()
                context = {"form": form}
                messages.error(request, "Session does not exist")
                return render(request, 'delete_session.html', context)
    else:
        form = delete_session_form()
        context = {"form": form}
        return render(request, 'delete_session.html', context)


def list_stadiums(request):
    mycursor = mydb.cursor()
    mycursor.execute("select s.stadium_name, s.stadium_country from stadium s")
    myresult = mycursor.fetchall()
    mycursor.close()
    context = {"stadiums": myresult}
    return render(request, 'list_stadiums.html', context)


def add_match(request):
    if request.method == "POST":
        form = add_match_form(request.POST)
        if form.is_valid():
            try:
                stadium_ID = form.cleaned_data["stadium_ID"]
                date = form.cleaned_data["date"]
                timeslot = form.cleaned_data["timeslot"]
                assigned_jury_name = form.cleaned_data["assigned_jury_name"]
                assigned_jury_surname = form.cleaned_data["assigned_jury_surname"]

                mycursor = mydb.cursor()

                mycursor.execute("select u.username from user u where u.name=%s and u.surname=%s", (assigned_jury_name, assigned_jury_surname))
                assigned_jury = mycursor.fetchone()
                if assigned_jury is None:
                    form = add_match_form()
                    context = {"form": form}
                    messages.error(request, "Jury does not exist")
                    return render(request, 'add_match.html', context)
                assigned_jury = assigned_jury[0]

                mycursor.execute("select m.session_ID from matchsession m order by m.session_ID desc limit 1")
                session_ID = mycursor.fetchone()
                if session_ID is None:
                    session_ID = 1
                else:
                    session_ID = session_ID[0] + 1

                mycursor.execute(
                    "select t.team_ID from team t where t.coach_username=%s and t.contract_start < %s and t.contract_finish > %s",
                    (request.session.get("username"), date, date))
                team_ID = mycursor.fetchone()
                if team_ID is None:
                    form = add_match_form()
                    context = {"form": form}
                    messages.error(request, "No team found for this coach")
                    return render(request, 'add_match.html', context)
                team_ID = team_ID[0]
                mycursor.execute("insert into matchsession (session_ID, team_ID, stadium_ID, time_slot, `date`, assigned_jury_username) values(%s, %s, %s, %s, %s, %s)", (session_ID, team_ID, stadium_ID, timeslot, date, assigned_jury))
                mydb.commit()
                mycursor.close()
                messages.success(request, "Match added successfully")
                return redirect("dashboard")
            except Exception as e:
                print(e)
                form = add_match_form()
                context = {"form": form}
                messages.error(request, "Something is wrong. Please try again.")
                return render(request, 'add_match.html', context)
        else:
            form = add_match_form()
            context = {"form": form}
            messages.error(request, "Invalid form")
            return render(request, 'add_match.html', context)
    else:
        form = add_match_form()
        context = {"form": form}
        return render(request, 'add_match.html', context)


def get_info(request):
    username = request.session.get("username")
    mycursor = mydb.cursor()
    mycursor.execute("select avg(rating), count(*) from matchsession m where m.assigned_jury_username=%s and m.rating is not null", (username,))
    info = mycursor.fetchone()
    info_dict = {"avg_rating": info[0], "number_of_matches": info[1]}

    return render(request, 'get_info.html', {"info_dict": info_dict})

def rate(request):
    if request.method == "POST":
        form = rate_form(request.POST)
        if form.is_valid():
            try:
                session_ID = form.cleaned_data["session_ID"]
                rating = form.cleaned_data["rating"]
                current_date = datetime.now().date()
                username = request.session.get("username")

                mycursor = mydb.cursor()
                mycursor.execute("update matchsession m set m.rating=%s where session_ID=%s and m.rating is null and  m.date < %s and m.assigned_jury_username = %s", (rating, session_ID, current_date, username))
                mydb.commit()
                mycursor.close()
                messages.success(request, "Rating added successfully if the jury was assigned to the match. Otherwise, the rating haven't been modified.")
                return redirect("dashboard")
            except Exception as e:
                form = rate_form()
                context = {"form": form}
                messages.error(request, "You should rate a match that has already happened. Please try again.")
                return render(request, 'rate.html', context)
    else:
        form = rate_form()
        context = {"form": form}
        return render(request, 'rate.html', context)



