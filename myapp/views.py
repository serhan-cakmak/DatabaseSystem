from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
import mysql.connector

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
                mycursor = mydb.cursor()
                mycursor.execute("select * from player u where u.username=%s", (username,))
                myresult = mycursor.fetchone()
                mycursor.close()

                if myresult:
                    print("here")
                    return redirect("player")

                mycursor = mydb.cursor()
                mycursor.execute("select * from coach u where u.username=%s", (username,))
                myresult = mycursor.fetchone()
                mycursor.close()
                if myresult:
                    return redirect("coach")

                return redirect("admin")

            else:
                form = user_form()
                context = {"form": form,
                           "message": "Invalid username or password"}

    else:
        print("here4")
        form = user_form()
        context = {"form": form}

    return render(request, 'home.html', context)


def player(request):
    return render(request, 'player.html')


def coach(request):
    return render(request, 'coach.html')


def admin(request):
    return render(request, 'admin.html')
