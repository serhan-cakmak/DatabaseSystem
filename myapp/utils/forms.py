from django import forms


class user_form(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class admin_form_select(forms.Form):
    table = forms.ChoiceField(choices=[("add", "add"), ("update", "update")])


class coach_form_select(forms.Form):
    table = forms.ChoiceField(
        choices=[("delete_session", "delete_session"), ("list_stadiums", "list_stadiums"), ("add_match", "add_match"), ("add_squad", "add_squad")])


class jury_form_select(forms.Form):
    table = forms.ChoiceField(choices=[("get_info", "get_info"), ("rate", "rate")])


class admin_form_add(forms.Form):
    table = forms.ChoiceField(choices=[("player", "player"), ("coach", "coach"), ("jury", "jury")])


class add_player_form(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    name = forms.CharField()
    surname = forms.CharField()
    date_of_birth = forms.DateField()
    height = forms.FloatField()
    weight = forms.FloatField()


class add_coach_form(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    name = forms.CharField()
    surname = forms.CharField()
    nationality = forms.CharField()


class add_jury_form(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    name = forms.CharField()
    surname = forms.CharField()
    nationality = forms.CharField()


class update_stadium_form(forms.Form):
    old_stadium_name = forms.CharField()
    new_stadium_name = forms.CharField()


class delete_session_form(forms.Form):
    session_id = forms.IntegerField()


class add_match_form(forms.Form):
    stadium_ID = forms.IntegerField()
    date = forms.DateField()
    timeslot = forms.IntegerField()
    assigned_jury_name = forms.CharField()
    assigned_jury_surname = forms.CharField()


class rate_form(forms.Form):
    session_ID = forms.IntegerField()
    rating = forms.FloatField()


class add_squad_form(forms.Form):
    session_ID = forms.IntegerField()
    player_name1 = forms.CharField()
    player_name2 = forms.CharField()
    player_name3 = forms.CharField()
    player_name4 = forms.CharField()
    player_name5 = forms.CharField()
    player_name6 = forms.CharField()

    @property
    def player_name_fields(self):
        return [f'player_name{i + 1}' for i in range(6)]