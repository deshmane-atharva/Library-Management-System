from flask import Flask, render_template, request, redirect, url_for, flash
from supabase import create_client
import supabase
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from werkzeug.wrappers import response

load_dotenv()

app = Flask(__name__)
app.secret_key = '@Co3338'  # Change this

print("os env:", os.environ)
print("dotenv:", os.getenv('https://kszswxjgkxsciqaqfyuy.supabase.co'))
print("dotenv:", os.getenv('sb_publishable_vc6h3-qD_mYczg9l9E-ToQ_nXgsfulN'))

# Supabase setup
supabase_client = supabase.create_client('https://kszswxjgkxsciqaqfyuy.supabase.co', 'sb_publishable_vc6h3-qD_mYczg9l9E-ToQ_nXgsfulN')


print("Supabase client created:", supabase_client)
# Email setup
EMAIL_USER = 'deshmaneatharva137@gmail.com'

EMAIL_PASS = '@8669760238Ma'

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['You have received the book from Department library'] = subject
    msg['deshmaneatharva137@gmail.com'] = EMAIL_USER
    msg['To'] = to_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, to_email, msg.as_string())

@app.route('/')
def index():
    print("Index page accessed")
    return render_template('index.html')

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mob']
        try:
            supabase_client.table('members').insert({'name': name, 'email': email, 'mobile': mobile}).execute()
            flash('Member added successfully!')
            return redirect(url_for('Member'))
        except Exception as e:
            print("Error inserting member:", e)
            flash('Failed to add member')
            return redirect(url_for('add_member'))
    return render_template('add_member.html')

@app.route('/Member', methods=['GET', 'POST', 'DELETE']) 
def Member():
    if request.method == 'POST':
        member_id = request.form['member_id']
        member_name = request.form['name']
        member_email = request.form['email']
        member_mob = request.form['mobile']
        supabase_client.table('members').insert({'member_id': member_id, 'name': member_name, 'email': member_email, 'mobile': member_mob}).execute()
        flash('Member added successfully!')
        return redirect(url_for('Member'))
    response = supabase_client.table('members').select('*').execute()
    print("members response data:", response.data)
    members = response.data
    return render_template('Member.html', members=members)

@app.route('/delete_member', methods=['POST'])
def delete_member():
    member_id = request.form.get('member_id')
    if member_id:
        try:
            supabase_client.table('members').delete().eq('member_id', member_id).execute()
            flash('Member deleted successfully!')
        except Exception as e:
            print("Error deleting member:", e)
            flash('Failed to delete member')
    else:
        flash('No member_id provided for deletion')
    return redirect(url_for('Member'))

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_name = request.form['book_name']
        book_id = request.form['book_id']
        supabase_client.table('books').insert({'book_name': book_name, 'book_id': book_id}).execute()
        flash('Book added successfully!')
        return redirect(url_for('books'))
    return render_template('add_book.html')

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        book_name = request.form['book_name']
        book_id = request.form['book_id']
        supabase_client.table('books').insert({'book_name': book_name, 'book_id': book_id}).execute()
        flash('Book added successfully!')
        return redirect(url_for('books'))
    response = supabase_client.table('books').select('*').execute()
    print("Books response data:", response.data)
    books = response.data
    return render_template('Book_Info.html', books=books)

@app.route('/delete_book', methods=['POST'])
def delete_book():
    book_id = request.form.get('book_id')
    if book_id:
        try:
            supabase_client.table('books').delete().eq('book_id', book_id).execute()
            flash('Book deleted successfully!')
        except Exception as e:
            print("Error deleting book:", e)
            flash('Failed to delete book')
    else:
        flash('No book_id provided for deletion')
    return redirect(url_for('books'))

@app.route('/Transaction', methods=['GET', 'POST'])
def Transaction():
    if request.method == 'POST':
        action = request.form.get('action')
   
        if action == 'issue':
            member_id = int(request.form.get('member_id', 0))
            book_id = int(request.form.get('book_id', 0))
            book_name = request.form.get('book_name', '')
            # Get member email
            try:
                resp = supabase_client.table('members').select('email').eq('member_id', member_id).execute()
            except Exception as e:
                print("Error fetching member:", e)
                flash('Failed to find member')
                return redirect(url_for('Transaction'))
            if not resp.data:
                flash('Member not found')
                return redirect(url_for('Transaction'))
            member = resp.data[0]
            issue_date = datetime.now()
            return_date = issue_date + timedelta(days=14)
            # Insert transaction (store book_name too)
            try:
                tx_resp = supabase_client.table('transactions').insert({
                    'book_id': book_id,
                    'member_id': member_id,
                    'issue_date': issue_date.isoformat(),
                    'status': 'Issued'
                }).execute()
            except Exception as e:
                print("Error inserting transaction:", e)
                flash('Failed to create transaction')
                return redirect(url_for('Transaction'))
        elif action == 'return':
            book_id = int(request.form.get('book_id', 0))
            # Get the latest issued transaction for this book
            try:
                trans_resp = supabase_client.table('transactions').select('id, member_id, issue_date').eq('book_id', book_id).eq('status', 'Issued').order('issue_date', desc=True).limit(1).execute()
            except Exception as e:
                print("Error fetching transaction:", e)
                flash('Failed to find issued transaction')
                return redirect(url_for('Transaction'))
            if not trans_resp.data:
                flash('No issued transaction found for this book.')
                return redirect(url_for('Transaction'))
            trans = trans_resp.data[0]
            member_id = trans.get('member_id')
            trans_id = trans.get('id') if 'id' in trans else None
            # Update transaction (preferentially by id)
            try:
                if trans_id:
                    supabase_client.table('transactions').update({'status': 'Received', 'return_date': datetime.now().isoformat()}).eq('id', trans_id).execute()
                else:
                    supabase_client.table('transactions').update({'status': 'Received', 'return_date': datetime.now().isoformat()}).eq('book_id', book_id).eq('issue_date', trans.get('issue_date')).execute()
            except Exception as e:
                print("Error updating transaction:", e)
                flash('Return processed but failed to update transaction')
                return redirect(url_for('Transaction'))
        return redirect(url_for('Transaction'))
    # Get Member and books for dropdowns
    try:
        Members = supabase_client.table('members').select('member_id,name').execute().data
    except Exception as e:
        print("Error fetching members for dropdown:", e)
        Members = []
    print("Members data:", Members)
    books = supabase_client.table('books').select('book_id, book_name').execute().data
    print("Books data:", books)
    return render_template('Book_Trans.html', Members=Members, books=books)

@app.route('/history', methods=['GET', 'POST'])
def history():
    try:
        response = supabase_client \
            .table('transactions') \
            .select('*, members(name), books(book_name)') \
            .execute()

        transactions = response.data
        print("Transaction history data:", transactions)
        return render_template('History.html', transactions=transactions)
    except Exception as e:
        print("Error fetching transaction history:", e)
        flash('Failed to load transaction history')
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)