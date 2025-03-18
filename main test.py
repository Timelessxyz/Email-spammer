  class EmailSpammer:
      def __init__(self):
          self.root = tk.Tk()
          self.root.title("Email Spammer")
          self.root.geometry("600x700")
          self.root.configure(bg='#2c3e50')
      
          # Style
          style = ttk.Style()
          style.configure('TButton', padding=5, font=('Helvetica', 10))
          style.configure('TLabel', background='#2c3e50', foreground='white', font=('Helvetica', 10))
          style.configure('TEntry', padding=5)

          # SMTP Server options
          self.smtp_servers = [
              'smtp.gmail.com',
              'smtp.mail.yahoo.com',
              'smtp.office365.com'
          ]

          # Create GUI elements
          self.create_gui()
      
      def create_gui(self):
          # Target email
          ttk.Label(self.root, text="Target Email:").pack(pady=5)
          self.target_email = ttk.Entry(self.root, width=50)
          self.target_email.pack(pady=5)

          # From email
          ttk.Label(self.root, text="From Email (optional):").pack(pady=5)
          self.from_email = ttk.Entry(self.root, width=50)
          self.from_email.pack(pady=5)

          # Subject
          ttk.Label(self.root, text="Subject:").pack(pady=5)
          self.subject = ttk.Entry(self.root, width=50)
          self.subject.pack(pady=5)

          # Message
          ttk.Label(self.root, text="Message:").pack(pady=5)
          self.message = tk.Text(self.root, width=50, height=10)
          self.message.pack(pady=5)

          # Number of emails
          ttk.Label(self.root, text="Number of Emails:").pack(pady=5)
          self.num_emails = ttk.Entry(self.root, width=20)
          self.num_emails.pack(pady=5)

          # Delay between emails
          ttk.Label(self.root, text="Delay between emails (seconds):").pack(pady=5)
          self.delay = ttk.Entry(self.root, width=20)
          self.delay.pack(pady=5)

          # Use Tor proxy
          self.use_tor = tk.BooleanVar()
          ttk.Checkbutton(self.root, text="Use Tor for anonymity", variable=self.use_tor).pack(pady=5)

          # Use random SMTP
          self.use_random_smtp = tk.BooleanVar()
          ttk.Checkbutton(self.root, text="Use random SMTP servers", variable=self.use_random_smtp).pack(pady=5)

          # Progress bar
          self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
          self.progress.pack(pady=10)

          # Start button
          self.start_button = ttk.Button(self.root, text="Start Spamming", command=self.start_spam)
          self.start_button.pack(pady=10)

          # Status label
          self.status_label = ttk.Label(self.root, text="Status: Ready")
          self.status_label.pack(pady=5)

      def setup_tor(self):
          if self.use_tor.get():
              socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
              socket.socket = socks.socksocket

      def send_email(self, target, subject, body):
          try:
              msg = MIMEMultipart()
              msg['Subject'] = subject
              msg['To'] = target
          
              if self.from_email.get():
                  msg['From'] = self.from_email.get()
              else:
                  msg['From'] = f"anonymous{random.randint(1000,9999)}@anonymous.com"

              msg.attach(MIMEText(body, 'plain'))

              # Choose random SMTP server if enabled
              if self.use_random_smtp.get():
                  smtp_server = random.choice(self.smtp_servers)
              else:
                  smtp_server = 'smtp.gmail.com'

              context = ssl.create_default_context()
              with smtplib.SMTP(smtp_server, 587) as server:
                  server.starttls(context=context)
                  server.send_message(msg)
              return True
          except Exception as e:
              print(f"Error sending email: {str(e)}")
              return False

      def start_spam(self):
          try:
              num_emails = int(self.num_emails.get())
              delay = float(self.delay.get())
          
              def spam_thread():
                  self.setup_tor()
                  sent = 0
              
                  for i in range(num_emails):
                      if self.send_email(
                          self.target_email.get(),
                          self.subject.get(),
                          self.message.get("1.0", tk.END)
                      ):
                          sent += 1
                      
                      progress = (i + 1) / num_emails * 100
                      self.progress['value'] = progress
                      self.status_label['text'] = f"Status: Sent {sent}/{num_emails} emails"
                      self.root.update()
                  
                      if i < num_emails - 1:
                          time.sleep(delay)
              
                  messagebox.showinfo("Complete", f"Finished sending {sent} emails!")
                  self.progress['value'] = 0
                  self.status_label['text'] = "Status: Ready"

              thread = threading.Thread(target=spam_thread)
              thread.start()
          
          except ValueError:
              messagebox.showerror("Error", "Please enter valid numbers for email count and delay!")

  if __name__ == "__main__":
      app = EmailSpammer()
      app.root.mainloop()