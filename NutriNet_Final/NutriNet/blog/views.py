from django.shortcuts import render, redirect
from users.models import Profile
from django.contrib.auth.decorators import login_required
from plotly.offline import plot
from plotly.graph_objs import Scatter
from django.contrib import messages
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
import openai

openai.api_key = "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"


def generate_response(data):
    res = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"You are a medical expert, who is professional in providing suggestions in mental health, diet and exercise. Give me a detailed advice, including analysis of data, diet improvements, exercise suggestions, and other additional deductions based on given information point vice - {data}",
        max_tokens=1000,
        temperature=0.7,
    )
    return res.choices[0].text.strip()


def chat_view(request):
    if request.method == 'POST':
        # Extract all form inputs
        avg = request.POST.get('avg', '')
        t_high = request.POST.get('t_high', '')
        hght = request.POST.get('hght', '')
        weight = request.POST.get('weight', '')
        age = request.POST.get('age', '')
        glv = request.POST.get('glv', '')
        spo = request.POST.get('spo', '')
        his = request.POST.get('his', '')

        # Combine all inputs into a single string, separated by space or any character you prefer
        data = f'{avg},{t_high},{hght},{weight},{age},{glv},{spo},{his}'

        # Get chat history from the form or initialize if not present
        chat_history = request.POST.get('chat_history', '')

        # Append the new user input to the chat history, but don't show it
        chat_history += '\nPatient : Analysis'

        # Generate the response based on the combined data
        res = generate_response(data)

        # Append the response to the chat history with the heading "NutriBot"
        chat_history += f'\n{res}\n'+'-'*84  # Dotted line separator

        return render(request, 'blog/home.html', {'chat_history': chat_history})
    return render(request, 'blog/home.html', {'chat_history': ''})

@login_required
def home(request):
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST,
                               request.FILES,
                               instance=request.user.profile)
    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, f'Your account has been updated successfully!')
        return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    try:
        profile_instance = request.users.profile
    except Profile.DoesNotExist:
        profile_instance = None
    context = {
        'title': 'Home',
        'u_form': u_form,
        'p_form': p_form,
        'profile_instance': profile_instance,
    }
    return render(request, 'blog/home.html',context)

@login_required
def about(request):
    return render(request, 'blog/about.html',{'title':'About'})

@login_required
def graph(request):
    x_data = [0, 1, 2, 3]
    y_data = [x ** 2 for x in x_data]
    z_data = [x ** 1.5 for x in x_data]

    trace1 = Scatter(x=x_data, y=y_data, mode='lines', name='Ideal Glucose Level', opacity=0.8, line=dict(color='green'))
    trace2 = Scatter(x=x_data, y=z_data, mode='lines', name='Your Glucose Level', line=dict(color='blue'))
    layout = dict(
        title='Glucose Level Chart',
        xaxis=dict(title='Day'),
        yaxis=dict(title='Glucose Levels'),
        title_x = 0.5
    )
    fig = dict(data=[trace1, trace2], layout=layout)
    plot_div = plot(fig, output_type='div')
    return render(request, "blog/graph.html", context={'plot_div': plot_div})
