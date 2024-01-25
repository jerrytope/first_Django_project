from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Contact, Blogs
from PyPDF2 import PdfFileReader
from django.core.mail.message import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.core import mail
# Create your views here.

def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def contact(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Hey just login and Use my website")
        return redirect('/login')
    if request.method == 'POST':
        fname = request.POST.get('name')
        femail = request.POST.get('email')
        fphone = request.POST.get('phone')
        fdescription = request.POST.get('desc')
        
        quary = Contact(name=fname, email=femail, phone_number=fphone, description=fdescription)
        quary.save()


        from_email=settings.EMAIL_HOST_USER
        connection=mail.get_connection()
        connection.open()
        email_message=mail.EmailMessage(f'Email from {fname}',f'UserEmail : {femail}\nUserPhoneNumber : {fphone}\n\n\n QUERY : {fdescription}',from_email,['ayoadetemitope009@gmail.com','jerrytope009@gmail.com'],connection=connection)
        # email_client=mail.EmailMessage('Arkprocoder Response','Thanks For Reaching us\n\narkprocoder.tech\n9986786453\nanees@arkprocoder.tech',from_email,[femail],connection=connection)
        connection.send_messages([email_message])
        connection.close()


        messages.info(request,"Thanks for reaching us, we would get back to you soon......")
        return redirect('/contact')
    return render(request, 'contact.html')

def handleblog(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Hey just login and Use my website")
        return redirect('/login')
    allposts = Blogs.objects.all()
    context = {'allposts':allposts}
    return render(request, 'handleblog.html', context)

def blog(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Hey just login and Use my website")
        return redirect('/login')
    if request.method == 'POST':
        fname = request.POST.get('name')
        ftitle = request.POST.get('Title')
        fimage = request.POST.get('image')
        fdescription = request.POST.get('desc')
        
        quary = Blogs(authname=fname, title=ftitle, img=fimage, description=fdescription)
        quary.save()

    return render(request, 'blog.html')

def service(request):
	return render(request, 'service.html')


def handlelogout(request):
    logout(request)
    messages.info(request, 'logout successfully')
    return redirect('/login')
    
    
    
def handlelogin(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password1')
        myuser = authenticate(username = uname, password = pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request, "Login successful")
            return redirect('/')
        else:
            messages.error(request, "invailed details")
            return redirect('/login')
    return render(request, 'login.html')

def handlesignup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        comfrimpassword = request.POST.get('password2')
        if password != comfrimpassword:
            messages.warning(request, "Password is incorrect")
            return redirect('/signup')
            
        # print(username, email, password, comfrimpassword)
        try:
            if User.objects.get(username = uname):
                messages.info(request, "Username is Taken")
                return redirect('/signup')
        except:
            pass
        
        try:
            if User.objects.get(email = email):
                messages.info(request, "Email is taken")
                return redirect('/signup')
        except:
            pass
        myuser =User.objects.create_user(uname, email, password)
        myuser.save()
        messages.info(request, "Signup is Successful Please Login ")
        return redirect('/login')
    return render(request, 'signup.html')


from PyPDF2 import PdfReader
from io import BytesIO
from gtts import gTTS

def extract_text(pdf_file):
    text = ""
    with BytesIO(pdf_file.read()) as file_buffer:
        pdf_reader = PdfReader(file_buffer)
        for page_number in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_number].extract_text()
    return text

def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        text = extract_text(pdf_file)

        # You can do something with the extracted text here, like saving it to the database or displaying it in the response.
        return HttpResponse(text)
    
    return render(request, 'upload_pdf.html')



def convert_to_audio(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Hey just login and Use my website")
        return redirect('/login')
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        text = extract_text(pdf_file)

        # Convert text to speech
        language = 'en'  # You can change the language code if needed
        audio_obj = gTTS(text=text, lang=language, slow=False)
        
        # Save the audio content in a BytesIO object
        audio_content = BytesIO()
        audio_obj.write_to_fp(audio_content)
        audio_content.seek(0)

        # Return the audio content as an HTTP response with the appropriate content type
        return HttpResponse(audio_content.read(), content_type='audio/mp3')

    return render(request, 'convert_to_audio.html')


from openai import OpenAI

def QandA(request):
    OPENAI_API_KEY = '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'
    client = OpenAI(api_key=OPENAI_API_KEY)
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        example_text = extract_text(pdf_file)
        response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
        {"role": "system", "content": "You are a helpful assistant to Create 10 multiple-choice questions based on the text with increasing levels of difficulty for students. Provide 4 options for each question and identify the correct answer. designed to output JSON."},
        {"role": "user", "content": example_text}
             ]
        )
        final = response.choices[0].message.content
        return HttpResponse(final)
    return render(request, 'QQ.html')


def search(request):
    query=request.GET['search']
    if len(query)>100:
        allPosts=Blogs.objects.none()
    else:
        allPostsTitle=Blogs.objects.filter(title__icontains=query)
        allPostsDescription=Blogs.objects.filter(description__icontains=query)
        allPosts=allPostsTitle.union(allPostsDescription)
    if allPosts.count()==0:
        messages.warning(request,"No Search Results")
    params={'allPosts':allPosts,'query':query}

    return render(request,'search.html',params)


