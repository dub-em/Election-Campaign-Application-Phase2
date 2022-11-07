def logs_schedule():
  from prefect import Flow,task
  from prefect.schedules import IntervalSchedule
  import datetime

  @task(max_retries=3, retry_delay=datetime.timedelta(minutes=30))
  def exec_logs():
    import os
    from email.message import EmailMessage
    import ssl
    import smtplib
    from datetime import datetime
    import datetime
    import heroku

    os.system("heroku logs -n 20 --app vast-island-32605 >> file.txt")

    #heroku logs -n 20 --app vast-island-32605 >> file.txt

    f = open("file.txt","r")
    df = f.read()

    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M")
    today = datetime.date.today()


    email_sender = 'georgemichaeldagogomaynard@gmail.com'
    email_password = ''
    email_receiver = ['michaeligbomezie@gmail.com','georgemichaeldagogo@gmail.com']

    #'michaeligbomezie@gmail.com',

    subject = "Heroku Execution Logs for Election Database on {}".format(today)
    body = "Execution logs below \n \n {}".format(df)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver, em.as_string())

    f.close()
    if os.path.exists("file.txt"):
      os.remove("file.txt")
    else:
      print("The file does not exist")

  def flow_logs(schedule=None):
      """
      this function is for the orchestraction/scheduling of this script
      """
      with Flow("logs",schedule=schedule) as flow:
          Extract_Transform = exec_logs()
      return flow


  schedule = IntervalSchedule(
      start_date = datetime.datetime.now() + datetime.timedelta(seconds = 2),
      interval = datetime.timedelta(hours=24)
  )
  flow=flow_logs(schedule)

  flow.run()


logs_schedule()