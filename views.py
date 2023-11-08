from django.shortcuts import render, redirect
from django.views import View
from django.db import connection

class DataListView(View):
    """
    This view displays a list of data from the 'employee' table.
    """

    template_name = 'todo_app/data_list.html'

    def get_data(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employee")
            data = cursor.fetchall()
        return data

    def get(self, request):
        data = self.get_data()
        return render(request, self.template_name, {'data': data, 'message': 'Data List'})

class DataActionView(View):
    """
    This is a base class for actions related to data, providing common functionality.
    """

    template_name = 'todo_app/edit_data.html'
    success_message = ''
    error_message = 'Error: Operation failed'

    def get_data(self, username):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employee WHERE username = %s", [username])
            return cursor.fetchone()

    def get(self, request, username):
        data = self.get_data(username)
        return render(request, self.template_name, {'data': data, 'username': username, 'message': 'Edit Data'})

    def post_data(self, username, new_username, age_param):
        pass

    def post(self, request, username):
        new_username = request.POST.get('username')
        age_param = request.POST.get('age')
        if self.post_data(username, new_username, age_param):
            return redirect('data_list')
        return render(request, self.template_name, {'message': self.error_message})

class AddDataView(DataActionView):
    """
    This view allows adding data to the 'employee' table.
    """

    template_name = 'todo_app/add_data.html'
    success_message = 'Data added successfully'
    error_message = 'Error: Data addition failed'

    def post_data(self, username, new_username, age_param):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO employee (username, age) VALUES (%s, %s)", [new_username, age_param])
            return cursor.rowcount == 1

class EditDataView(DataActionView):
    """
    This view allows editing data in the 'employee' table.
    """

    success_message = 'Data updated successfully'
    error_message = 'Error: Data update failed'

    def post_data(self, username, new_username, age_param):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE employee SET username = %s, age = %s WHERE username = %s", [new_username, age_param, username])
            return cursor.rowcount == 1

class DeleteDataView(DataActionView):
    """
    This view allows deleting data from the 'employee' table.
    """

    template_name = 'todo_app/delete_data.html'
    success_message = 'Data deleted successfully'
    error_message = 'Error: Data deletion failed'

    def post_data(self, username, new_username, age_param):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM employee WHERE username = %s", [username])
            return cursor.rowcount == 1
