# Recommendation for logged-in customer
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def customer_recommendation(request):
    user_id = request.session.get('userid')
    if not user_id:
        return render(request, 'Customer/CustomerHome.html', {'msg': 'Please log in to see recommendations.'})
    user_id = int(user_id)
    import pymysql
    con = pymysql.connect(host='localhost', user='root', password='', database='service_portal', charset='utf8')
    df = pd.read_sql("SELECT user_id, product_id FROM product_book WHERE status='Accepted'", con)
    if df.empty or user_id not in df['user_id'].values:
        return render(request, 'Customer/CustomerHome.html', {'msg': 'No recommendations available yet.'})

    user_product = df.pivot_table(index='user_id', columns='product_id', aggfunc=len, fill_value=0)
    X = user_product.values
    y = user_product.idxmax(axis=1)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    joblib.dump(clf, 'rf_recommender.pkl')

    user_idx = list(user_product.index).index(user_id)
    user_vector = X[user_idx].reshape(1, -1)
    pred = clf.predict(user_vector)
    recommended_product_id = pred[0]

    cur = con.cursor()
    cur.execute("SELECT pname FROM product WHERE id=%s", (recommended_product_id,))
    row = cur.fetchone()
    product_name = row[0] if row else 'Unknown'

    return render(request, 'Customer/CustomerHome.html', {'recommendation': f'Recommended for you: {product_name}'})
from django.shortcuts import render
# import pymysql
from AdminApp.views import fetch_image_blob_from_product
import base64
# Create your views here.
def index(request):
    return render(request,'index.html')
def login(request):
    return render(request,'Customer/Login.html')

def Register(request):
    return render(request,'Customer/Register.html')

def RegAction(request):
    if request.method == 'POST' and request.FILES['image']:
        name=request.POST['name']
        email=request.POST['email']
        mobile=request.POST['mobile']
        image=request.FILES['image'].read()
        username=request.POST['username']
        password=request.POST['password']
        status='waiting'

        con=pymysql.connect(host='localhost', user='root',password='', database='service_portal', charset='utf8')
        cur=con.cursor()
        cur.execute("select * from register where  email='"+email+"' and mobile='"+mobile+"'")
        d=cur.fetchone()
        if d is not None:

         context={'msg':'Already Exist These Details...!!'}
         return render(request,'Customer/Register.html', context)
        else:
            cur=con.cursor()
            cur.execute('insert into register values(null,%s,%s,%s,%s,%s,%s,%s)',(name,email,mobile,image,username,password,status))
            con.commit()
            context={'msg':'Successfully Registered Your Details...!!'}
            return render(request,'Customer/Register.html', context)

def LogAction(request):
    uname=request.POST['username']
    pwd=request.POST['password']

    con=pymysql.connect(host='localhost', user='root', password='', database='service_portal', charset='utf8')
    cur=con.cursor()
    cur.execute("select * from register where username='"+uname+"' and password='"+pwd+"'")
    d=cur.fetchone()
    if d is not None:
        request.session['userid']=d[0]
        request.session['name']=d[1]
        request.session['email']=d[2]
        return render(request, 'Customer/CustomerHome.html')
    else:
        context={'msg':'Login Failed...!!'}
        return render(request, 'Customer/Login.html',context)

def CustomerHome(request):
    # Show recommendation automatically
    user_id = request.session.get('userid')
    if not user_id:
        return render(request, 'Customer/CustomerHome.html', {'msg': 'Please log in to see recommendations.'})
    user_id = str(user_id)
    import pymysql
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import joblib
    con = pymysql.connect(host='localhost', user='root', password='', database='service_portal', charset='utf8')
    df = pd.read_sql("SELECT user_id, product_id FROM product_book WHERE status='Accepted'", con)
    if df.empty or user_id not in df['user_id'].values:
        return render(request, 'Customer/CustomerHome.html', {'msg': 'No recommendations available yet.'})

    user_product = df.pivot_table(index='user_id', columns='product_id', aggfunc=len, fill_value=0)
    X = user_product.values
    y = user_product.idxmax(axis=1)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    joblib.dump(clf, 'rf_recommender.pkl')

    user_idx = list(user_product.index).index(user_id)
    user_vector = X[user_idx].reshape(1, -1)
    pred = clf.predict(user_vector)
    recommended_product_id = pred[0]

    cur = con.cursor()
    cur.execute("SELECT pname FROM product WHERE id=%s", (recommended_product_id,))
    row = cur.fetchone()
    product_name = row[0] if row else 'Unknown'

    return render(request, 'Customer/CustomerHome.html', {'recommendation': f'Recommended for you: {product_name}'})

def ViewService(request):
    con=pymysql.connect(host='localhost', user='root',password='', database='service_portal', charset='utf8')
    cur=con.cursor()

    cur.execute("select * from sregister")
    data=cur.fetchall()
    table="<table><tr><th>Service Name</th><th>Email</th><th>Mobile</th><th>Working Hours</th><th>Cost</th><th>Book</th></tr>"
    for d in data:
        table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[7])+"</td><td>"+str(d[5])+"</td><td>Rs."+str(d[6])+"</td><td><a href='BookService?sid="+str(d[0])+"'>Book Now</a></td></tr>"
    table+="</table>"
    context={'data':table}
    return render(request,'Customer/ViewServices.html', context)
def BookService(request):
    service_id=request.GET['sid']
    uid=request.session['userid']
    user_id=str(uid)

    con=pymysql.connect(host='localhost', user='root',password='', database='service_portal', charset='utf8')
    cur=con.cursor()
    cur.execute("insert into service_book values(null,'"+user_id+"','"+service_id+"',now(),'waiting')")
    con.commit()
    cur.execute("select * from sregister")
    data=cur.fetchall()
    table="<table><tr><th>Service Name</th><th>Email</th><th>Mobile</th><th>Working Hours</th><th>Cost</th><th>Book</th></tr>"
    for d in data:
        table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[7])+"</td><td>"+str(d[5])+"</td><td>Rs."+str(d[6])+"</td><td><a href='BookService?sid="+str(d[0])+"'>Book Now</a></td></tr>"
    table+="</table>"
    context={'data':table,'msg':'Booking Successful ...!!'}
    return render(request,'Customer/ViewServices.html', context)


def ViewProducts(request):
    con=pymysql.connect(host='localhost', user='root',password='', database='service_portal', charset='utf8')
    cur=con.cursor()

    cur.execute("select * from product")
    data=cur.fetchall()
    table="<table><tr><th>Product Name</th><th>Price</th><th>Product Usage</th><th>Product Image</th></tr>"
    for d in data:
        iid=d[0]
        image_blob = fetch_image_blob_from_product(iid)
        image_base64 = base64.b64encode(image_blob).decode('utf-8')
        table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+" Rs.</td><td>"f'<img src="data:image/png;base64,{image_base64}" alt="Image" />'"</td><td><a href='CartProduct?pid="+str(d[0])+"&pr="+str(d[2])+"'>Cart</a></td></tr>"
    table+="</table>"
    context={'data':table}
    return render(request,'Customer/ViewProducts.html', context)

def CartProduct(request):
    pid=request.GET['pid']
    ppid=str(pid)
    p=request.GET['pr']

    uid=request.session['userid']
    user_id=str(uid)
    con=pymysql.connect(host='localhost', user='root',password='', database='service_portal', charset='utf8')
    curr=con.cursor()
    curr.execute("select count(*) from cart where u_id='"+user_id+"'and p_id='"+ppid+"'")
    c=curr.fetchone()
    if c[0]==0:
        cur=con.cursor()
        cur.execute("insert into cart values(null,'"+user_id+"','"+ppid+"','"+p+"','waiting')")
        con.commit()

        cur1=con.cursor()
        cur1.execute("select * from product")
        data=cur1.fetchall()
        table="<table><tr><th>Product Name</th><th>Price</th><th>Product Usage</th><th>Product Image</th></tr>"
        for d in data:
            iid=d[0]
            image_blob = fetch_image_blob_from_product(iid)
            image_base64 = base64.b64encode(image_blob).decode('utf-8')
            table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+" Rs.</td><td>"f'<img src="data:image/png;base64,{image_base64}" alt="Image" />'"</td><td><a href='CartProduct?pid="+str(d[0])+"&pr="+str(d[2])+"'>Cart</a></td></tr>"
        table+="</table>"

        context={'data':table,'msg':'Product Added To cart'}
        return render(request,'Customer/ViewProducts.html', context)
    else:
        cur1=con.cursor()
        cur1.execute("select * from product")
        data=cur1.fetchall()
        table="<table><tr><th>Product Name</th><th>Price</th><th>Product Usage</th><th>Product Image</th></tr>"
        for d in data:
            iid=d[0]
            image_blob = fetch_image_blob_from_product(iid)
            image_base64 = base64.b64encode(image_blob).decode('utf-8')
            table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+" Rs.</td><td>"f'<img src="data:image/png;base64,{image_base64}" alt="Image" />'"</td><td><a href='CartProduct?pid="+str(d[0])+"&pr="+str(d[2])+"'>Cart</a></td></tr>"
        table+="</table>"

        context={'data':table,'msg':'Product Already Added To cart'}
        return render(request,'Customer/ViewProducts.html', context)



def ViewCart(request):
    uid=request.session['userid']
    user_id=str(uid)

    con=pymysql.connect(host='localhost', user='root',password='', database='service_portal', charset='utf8')
    cur=con.cursor()

    cur.execute("select * from product p,cart c where p.id=c.p_id and u_id='"+user_id+"'")
    data=cur.fetchall()
    table="<table><tr><th>Product Name</th><th>Price</th><th>Product Image</th></tr>"
    total=0
    for d in data:
        iid=d[0]
        image_blob = fetch_image_blob_from_product(iid)
        image_base64 = base64.b64encode(image_blob).decode('utf-8')
        total+=int(d[8])
        table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+" Rs.</td><td>"f'<img src="data:image/png;base64,{image_base64}" alt="Image" style="border-radius:100px;"/>'"</td></tr>"
    tr=str(total)
    table+="<tr><td>TOTAL </td><td>"+tr+"</td><td><input type='submit' value='Buy Now'></td></tr"
    table+="</table>"
    context={'data':table}
    return render(request,'Customer/ViewCartProducts.html', context)

def CartAction(request):
    return render(request,'Customer/Payment.html')


def BookProduct(request):
    uid=request.session['userid']
    user_id=str(uid)

    con=pymysql.connect(host='localhost', user='root',password='', database='service_portal', charset='utf8')
    cur1=con.cursor()
    cur1.execute("select * from cart where u_id='"+user_id+"'")
    dd=cur1.fetchall()
    curr=con.cursor()
    if dd is not None:
        for k in dd:
            ppi=str(k[2])
            cur=con.cursor()
            i=cur.execute("insert into product_book values(null,'"+user_id+"','"+ppi+"',now(),'waiting')")
            print(i)
            con.commit()

        curr.execute("delete from cart where u_id='"+user_id+"'")
        con.commit()
        cur11=con.cursor()
        cur11.execute("select * from product")
        data=cur11.fetchall()
        table="<table><tr><th>Product Name</th><th>Price</th><th>Product Usage</th><th>Product Image</th></tr>"
        for d in data:
            iid=d[0]
            image_blob = fetch_image_blob_from_product(iid)
            image_base64 = base64.b64encode(image_blob).decode('utf-8')
            table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+" Rs.</td><td>"f'<img src="data:image/png;base64,{image_base64}" alt="Image" />'"</td><td><a href='CartProduct?pid="+str(d[0])+"&pr="+str(d[2])+"'>Cart</a></td></tr>"
        table+="</table>"
        context={'data':table,'msg':'Product Booked Successfully..!!'}
        return render(request,'Customer/ViewProducts.html', context)



    else:
        cur11=con.cursor()
        cur11.execute("select * from product")
        data=cur11.fetchall()
        table="<table><tr><th>Product Name</th><th>Price</th><th>Product Usage</th><th>Product Image</th></tr>"
        for d in data:
            iid=d[0]
            image_blob = fetch_image_blob_from_product(iid)
            image_base64 = base64.b64encode(image_blob).decode('utf-8')
            table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+" Rs.</td><td>"f'<img src="data:image/png;base64,{image_base64}" alt="Image" />'"</td><td><a href='CartProduct?pid="+str(d[0])+"&pr="+str(d[2])+"'>Cart</a></td></tr>"
        table+="</table>"
        context={'data':table,'msg':'Product Booked Successfully..!!'}
        return render(request,'Customer/ViewProducts.html', context)




def viewbookings(request):
    uid=request.session['userid']
    user_id=str(uid)
    con=pymysql.connect(host='localhost', user='root',password='', database='service_portal', charset='utf8')
    cur=con.cursor()
    cur.execute("select * from product_book pb, product p where p.id=pb.product_id and pb.user_id='"+user_id+"'")
    data=cur.fetchall()
    table="<table><tr><th>Product Name</th><th>Price</th><th>Image</th><th>Booked Date</th><th>Status</th><tr>"
    for d in data:
        iid=d[5]
        image_blob = fetch_image_blob_from_product(iid)
        image_base64 = base64.b64encode(image_blob).decode('utf-8')
        table+="<tr><td>"+str(d[6])+"</td><td>"+str(d[7])+"</td><td>"f'<img src="data:image/png;base64,{image_base64}" alt="Image" />'"</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td></tr>"
    table+="</table>"

    cur1=con.cursor()
    cur1.execute("select * from service_book sb, sregister sr where sb.service_id=sr.id and sb.userid='"+user_id+"'")
    data=cur1.fetchall()
    srtable="<table><tr><th>Service Name</th><th>Email</th><th>Mobile</th><th>Working Hours</th><th>Cost</th><th>Booked Date</th><th>Booking Status</th></tr>"
    for d in data:
        srtable+="<tr><td>"+str(d[6])+"</td><td>"+str(d[7])+"</td><td>"+str(d[12])+"</td><td>"+str(d[10])+"</td><td>Rs."+str(d[11])+"</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td></tr>"
    srtable+="</table>"
    context={'data':table,'servicetable':srtable}
    return render(request,'Customer/ViewAllBookings.html', context)




