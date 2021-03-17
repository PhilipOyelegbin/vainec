# Vote Arbiter INEC
from flask import Flask, render_template, request
import mysql.connector as sql
import matplotlib as mpl
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import base64
import time


app = Flask(__name__)

con = sql.connect(host="sql2.freemysqlhosting.net", user="sql2385508", passwd="cI3*uZ9%", database="sql2385508")
cur = con.cursor()
cur.execute("SELECT * FROM DateTime")
rows = cur.fetchall()
for row in rows:
    start_d = row[0]
    start_t = row[1]
    end_d = row[2]
    end_t = row[3]

# Close the voting site
commence = start_d + ", " + start_t
deadline = end_d + ", " + end_t
today = time.strftime("%Y-%m-%d, %I:%M:%p")
print(today)

def vote(Table):
    if request.method == "POST":
        try:
            pvc = request.form ['pvc']
            party = request.form ['political_party']
            date = time.strftime('%A, %d-%D-%Y')
            timer = time.strftime('%I:%M:%p')
            # Validate PVC
            con = sql.connect(host="sql2.freemysqlhosting.net", user="sql2385508", passwd="cI3*uZ9%", database="sql2385508")
            cur = con.cursor()
            cur.execute("SELECT * FROM PVC WHERE ID = %s", [pvc])
            validate = cur.fetchall()
            if not validate:
                state = "Voter not registered"
            else:
                cur.execute("SELECT * FROM " + Table + " WHERE PVC = %s", [pvc])
                rows = cur.fetchall()
                if rows:
                    state = "Voter already voted.\nMultiple voting not allowed."
                else:
                    cur.execute("INSERT INTO " + Table + " (PVC, Party, Date, Time) VALUES (%s, %s, %s, %s)", [pvc, party, date, timer])
                    con.commit()
                    state = 'Vote successful.'
        except:
            con.rollback()
            state = "error in insert operation"
        finally:
            return (state)


def res(Table):
    with sql.connect(host="sql2.freemysqlhosting.net", user="sql2385508", passwd="cI3*uZ9%", database="sql2385508") as con:
        img = BytesIO()
        data = pd.read_sql("SELECT * FROM " + Table, con)
        aa = (data['Party'] == "AA").sum()
        aac = (data['Party'] == "AAC").sum()
        accord = (data['Party'] == "ACCORD").sum()
        adc = (data['Party'] == "ADC").sum()
        adp = (data['Party'] == "ADP").sum()
        apc = (data['Party'] == "APC").sum()
        apga = (data['Party'] == "APGA").sum()
        apm = (data['Party'] == "APM").sum()
        app = (data['Party'] == "APP").sum()
        boot = (data['Party'] == "BOOT").sum()
        lp = (data['Party'] == "LP").sum()
        nnpp = (data['Party'] == "NNPP").sum()
        nrm = (data['Party'] == "NRM").sum()
        pdp = (data['Party'] == "PDP").sum()
        prp = (data['Party'] == "PRP").sum()
        sdp = (data['Party'] == "SDP").sum()
        ypp = (data['Party'] == "YPP").sum()
        zlp = (data['Party'] == "ZLP").sum()
        
        # Bar Chart
        mpl.style.use(['ggplot'])
        labels = ("AA", "AAC", "ACCORD", "ADC", "ADP", "APC", "APGA", "APM", "APP", "BOOT", "LP", "NNPP", "NRM", "PDP", "PRP", "SDP", "YPP", "ZLP") # provides labels on x axis
        index = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18) # provides locations on x axis
        sizes = [aa, aac, accord, adc, adp, apc, apga, apm, app, boot, lp, nnpp, nrm, pdp, prp, sdp, ypp, zlp] # provides values on y axis
        plt.barh(index, sizes, tick_label=labels, color='steelblue')
        plt.title("Voting Result", fontsize=12)
        plt.ylabel('Parties', fontsize=12)
        plt.xlabel('Number of Votes', fontsize=12)
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        plot = base64.b64encode(img.getvalue()).decode('utf8')
        return (plot)


# Home Page
@app.route('/')
def home():
    if today > deadline:
        timer = "Voting closed!"
    elif today > commence:
        timer = "Voting will close [" + deadline + "]"
    else:
        timer = "Voting will start [" + commence + "]"
    return render_template('home.html', info=timer)

# Verifiation Page
@app.route('/admin')
def admin():
    return render_template('log_in.html')

# log_in function
@app.route('/log_in', methods = ["POST", "GET"])
def log_in():
    if request.method == "POST":
        username = request.form ['Username']
        password = request.form ['Password']
        if username != "oyetek" or password != "1234":
            alert = "Incorrect Username or Password"
            return render_template('log_in.html', alarm=alert)
        else:
            time.sleep(0.1)
            return render_template('admin.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')


# President Page
@app.route('/president')
def president():
    return render_template('president.html', result=res("President"))

# States Page
@app.route('/abia')
def abia():
    return render_template('abia.html', result=res("AbiaState"))

@app.route('/adamawa')
def adamawa():
    return render_template('adamawa.html', result=res("AdamawaState"))

@app.route('/akwaibom')
def akwaibom():
    return render_template('akwaibom.html', result=res("AkwaIbomState"))

@app.route('/anambra')
def anambra():
    return render_template('anambra.html', result=res("AnambraState"))

@app.route('/bauchi')
def bauchi():
    return render_template('bauchi.html', result=res("BauchiState"))

@app.route('/bayelsa')
def bayelsa():
    return render_template('bayelsa.html', result=res("BayelsaState"))

@app.route('/benue')
def benue():
    return render_template('benue.html', result=res("BenueState"))

@app.route('/borno')
def borno():
    return render_template('borno.html', result=res("BornoState"))

@app.route('/crossriver')
def crossriver():
    return render_template('crossriver.html', result=res("CrossRiverState"))

@app.route('/delta')
def delta():
    return render_template('delta.html', result=res("DeltaState"))

@app.route('/ebonyi')
def ebonyi():
    return render_template('ebonyi.html', result=res("EbonyiState"))

@app.route('/edo')
def edo():
    return render_template('edo.html', result=res("EdoState"))

@app.route('/ekiti')
def ekiti():
    return render_template('ekiti.html', result=res("EkitiState"))

@app.route('/enugu')
def enugu():
    return render_template('enugu.html', result=res("EnuguState"))
    
@app.route('/gombe')
def gombe():
    return render_template('gombe.html', result=res("GombeState"))

@app.route('/imo')
def imo():
    return render_template('imo.html', result=res("ImoState"))

@app.route('/jigawa')
def jigawa():
    return render_template('jigawa.html', result=res("JigawaState"))

@app.route('/kaduna')
def kaduna():
    return render_template('kaduna.html', result=res("KadunaState"))

@app.route('/kano')
def kano():
    return render_template('kano.html', result=res("KanoState"))

@app.route('/kastina')
def kastina():
    return render_template('kastina.html', result=res("KastinaState"))

@app.route('/kebbi')
def kebbi():
    return render_template('kebbi.html', result=res("KebbiState"))

@app.route('/kogi')
def kogi():
    return render_template('kogi.html', result=res("KogiState"))

@app.route('/kwara')
def kwara():
    return render_template('kwara.html', result=res("KwaraState"))

@app.route('/lagos')
def lagos():
    return render_template('lagos.html', result=res("LagosState"))

@app.route('/nasarawa')
def nasarawa():
    return render_template('nasarawa.html', result=res("NasarawaState"))

@app.route('/niger')
def niger():
    return render_template('niger.html', result=res("NigerState"))

@app.route('/ogun')
def ogun():
    return render_template('ogun.html', result=res("OgunState"))

@app.route('/ondo')
def ondo():
    return render_template('ondo.html', result=res("OndoState"))

@app.route('/osun')
def osun():
    return render_template('osun.html', result=res("OsunState"))

@app.route('/oyo')
def oyo():
    return render_template('oyo.html', result=res("OyoState"))

@app.route('/plateau')
def plateau():
    return render_template('plateau.html', result=res("PlateauState"))

@app.route('/rivers')
def rivers():
    return render_template('rivers.html', result=res("RiversState"))

@app.route('/sokoto')
def sokoto():
    return render_template('sokoto.html', result=res("SokotoState"))

@app.route('/taraba')
def taraba():
    return render_template('taraba.html', result=res("TarabaState"))

@app.route('/yobe')
def yobe():
    return render_template('yobe.html', result=res("YobeState"))

@app.route('/zamfara')
def zamfara():
    return render_template('zamfara.html', result=res("ZamfaraState"))


# vote_president function
@app.route('/president', methods = ["POST", "GET"])
def vote_president():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("President")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_abia function
@app.route('/abia', methods = ["POST", "GET"])
def vote_abia():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("AbiaState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_adamawa function
@app.route('/adamawa', methods = ["POST", "GET"])
def vote_adamawa():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("AdamawaState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_akwaibom function
@app.route('/akwaibom', methods = ["POST", "GET"])
def vote_akwaibom():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("AkwaIbomState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_anambra function
@app.route('/anambra', methods = ["POST", "GET"])
def vote_anambra():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("AnambraState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_bauchi function
@app.route('/bauchi', methods = ["POST", "GET"])
def vote_bauchi():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("BauchiState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_bayelsa function
@app.route('/bayelsa', methods = ["POST", "GET"])
def vote_bayelsa():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("BayelsaState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_benue function
@app.route('/benue', methods = ["POST", "GET"])
def vote_benue():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("BenueState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_borno function
@app.route('/borno', methods = ["POST", "GET"])
def vote_borno():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("BornoState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_crossriver function
@app.route('/crossriver', methods = ["POST", "GET"])
def vote_crossriver():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("CrossRiverState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_delta function
@app.route('/delta', methods = ["POST", "GET"])
def vote_delta():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("DeltaState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_ebonyi function
@app.route('/ebonyi', methods = ["POST", "GET"])
def vote_ebonyi():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("EbonyiState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_edo function
@app.route('/edo', methods = ["POST", "GET"])
def vote_edo():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("EdoState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_ekiti function
@app.route('/ekiti', methods = ["POST", "GET"])
def vote_ekiti():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("EkitiState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_enugu function
@app.route('/enugu', methods = ["POST", "GET"])
def vote_enugu():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("EnuguState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_gombe function
@app.route('/gombe', methods = ["POST", "GET"])
def vote_gombe():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("GombeState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_imo function
@app.route('/imo', methods = ["POST", "GET"])
def vote_imo():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("ImoState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_jigawa function
@app.route('/jigawa', methods = ["POST", "GET"])
def vote_jigawa():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("JigawaState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_kaduna function
@app.route('/kaduna', methods = ["POST", "GET"])
def vote_kaduna():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("KadunaState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_kano function
@app.route('/kano', methods = ["POST", "GET"])
def vote_kano():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("KanoState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_kastina function
@app.route('/kastina', methods = ["POST", "GET"])
def vote_kastina():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("KastinaState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_kebbi function
@app.route('/kebbi', methods = ["POST", "GET"])
def vote_kebbi():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("KebbiState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_kogi function
@app.route('/kogi', methods = ["POST", "GET"])
def vote_kogi():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("KogiState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_kwara function
@app.route('/kwara', methods = ["POST", "GET"])
def vote_kwara():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("KwaraState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_lagos function
@app.route('/lagos', methods = ["POST", "GET"])
def vote_lagos():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("LagosState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_nasarawa function
@app.route('/nasarawa', methods = ["POST", "GET"])
def vote_nasarawa():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("NasarawaState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_niger function
@app.route('/niger', methods = ["POST", "GET"])
def vote_niger():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("NigerState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_ogun function
@app.route('/ogun', methods = ["POST", "GET"])
def vote_ogun():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("OgunState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_ondo function
@app.route('/ondo', methods = ["POST", "GET"])
def vote_ondo():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("OndoState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_osun function
@app.route('/osun', methods = ["POST", "GET"])
def vote_osun():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("OsunState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_oyo function
@app.route('/oyo', methods = ["POST", "GET"])
def vote_oyo():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("OyoState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_plateau function
@app.route('/plateau', methods = ["POST", "GET"])
def vote_plateau():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("PlateauState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_rivers function
@app.route('/rivers', methods = ["POST", "GET"])
def vote_rivers():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("RiversState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_sokoto function
@app.route('/sokoto', methods = ["POST", "GET"])
def vote_sokoto():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("SokotoState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_taraba function
@app.route('/taraba', methods = ["POST", "GET"])
def vote_taraba():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("TarabaState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_yobe function
@app.route('/yobe', methods = ["POST", "GET"])
def vote_yobe():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("YobeState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)

# vote_zamfara function
@app.route('/zamfara', methods = ["POST", "GET"])
def vote_zamfara():
    if today > deadline:
        state = "Voting closed!"
    elif today > commence:
        state = vote("ZamfaraState")
    else:
        state = "Voting will start [" + commence + "]"
    return render_template('feedback.html', status=state)


# set_time function
@app.route('/set_time', methods = ["POST", "GET"])
def set_time():
    if request.method == "POST":
        try:
            start_date = request.form ['start_date']
            start_time = request.form ['start_time']
            end_date = request.form ['end_date']
            end_time = request.form ['end_time']
            con = sql.connect(host="sql2.freemysqlhosting.net", user="sql2385508", passwd="cI3*uZ9%", database="sql2385508")
            cur = con.cursor()
            cur.execute("DELETE FROM DateTime")
            cur.execute("INSERT INTO DateTime (StartDate, StartTime, EndDate, EndTime) VALUES (%s, %s, %s, %s)", [start_date, start_time, end_date, end_time])
            con.commit()
            status = 'Timer Set.'
        except:
            con.rollback()
            status = "error in insert operation"
        finally:
            return render_template('admin.html', timer=status)


# reset function
@app.route('/db_reset', methods = ["POST", "GET"])
def db_reset():
    if request.method == "POST":
        database = request.form ['db']
        con = sql.connect(host="sql2.freemysqlhosting.net", user="sql2385508", passwd="cI3*uZ9%", database="sql2385508")
        cur = con.cursor()
        if "President" == database:
            cur.execute("DELETE FROM President")
        elif "Abia" == database:
            cur.execute("DELETE FROM AbiaState")
        elif "Adamawa" == database:
            cur.execute("DELETE FROM AdamawaState")
        elif "Akwaibom" == database:
            cur.execute("DELETE FROM AkwaIbomState")
        elif "Anambra" == database:
            cur.execute("DELETE FROM AnambraState")
        elif "Bauchi" == database:
            cur.execute("DELETE FROM BauchiState")
        elif "Bayelsa" == database:
            cur.execute("DELETE FROM BayelsaState")
        elif "Benue" == database:
            cur.execute("DELETE FROM BenueState")
        elif "Borno" == database:
            cur.execute("DELETE FROM BornoState")
        elif "Crossriver" == database:
            cur.execute("DELETE FROM CrossRiverState")
        elif "Delta" == database:
            cur.execute("DELETE FROM DeltaState")
        elif "Ebonyi" == database:
            cur.execute("DELETE FROM EbonyiState")
        elif "Edo" == database:
            cur.execute("DELETE FROM EdoState")
        elif "Ekiti" == database:
            cur.execute("DELETE FROM EkitiState")
        elif "Enugu" == database:
            cur.execute("DELETE FROM EnuguState")
        elif "Gombe" == database:
            cur.execute("DELETE FROM GombeState")
        elif "Imo" == database:
            cur.execute("DELETE FROM ImoState")
        elif "Jigawa" == database:
            cur.execute("DELETE FROM JigawaState")
        elif "Kaduna" == database:
            cur.execute("DELETE FROM KadunaState")
        elif "Kano" == database:
            cur.execute("DELETE FROM KanoState")
        elif "Kastina" == database:
            cur.execute("DELETE FROM KastinaState")
        elif "Kebbi" == database:
            cur.execute("DELETE FROM KebbiState")
        elif "Kogi" == database:
            cur.execute("DELETE FROM KogiState")
        elif "Kwara" == database:
            cur.execute("DELETE FROM KwaraState")
        elif "Lagos" == database:
            cur.execute("DELETE FROM LagosState")
        elif "Nasarawa" == database:
            cur.execute("DELETE FROM NasarawaState")
        elif "Niger" == database:
            cur.execute("DELETE FROM NigerState")
        elif "Ogun" == database:
            cur.execute("DELETE FROM OgunState")
        elif "Ondo" == database:
            cur.execute("DELETE FROM OndoState")
        elif "Osun" == database:
            cur.execute("DELETE FROM OsunState")
        elif "Oyo" == database:
            cur.execute("DELETE FROM OyoState")
        elif "Plateau" == database:
            cur.execute("DELETE FROM PlateauState")
        elif "Rivers" == database:
            cur.execute("DELETE FROM RiversState")
        elif "Sokoto" == database:
            cur.execute("DELETE FROM SokotoState")
        elif "Taraba" == database:
            cur.execute("DELETE FROM TarabaState")
        elif "Yobe" == database:
            cur.execute("DELETE FROM YobeState")
        elif "Zamfara" == database:
            cur.execute("DELETE FROM ZamfaraState")
        else:
            cur.execute("DELETE FROM President")
            cur.execute("DELETE FROM AbiaState")
            cur.execute("DELETE FROM AdamawaState")
            cur.execute("DELETE FROM AkwaIbomState")
            cur.execute("DELETE FROM AnambraState")
            cur.execute("DELETE FROM BauchiState")
            cur.execute("DELETE FROM BayelsaState")
            cur.execute("DELETE FROM BenueState")
            cur.execute("DELETE FROM BornoState")
            cur.execute("DELETE FROM CrossRiverState")
            cur.execute("DELETE FROM DeltaState")
            cur.execute("DELETE FROM EbonyiState")
            cur.execute("DELETE FROM EdoState")
            cur.execute("DELETE FROM EkitiState")
            cur.execute("DELETE FROM EnuguState")
            cur.execute("DELETE FROM GombeState")
            cur.execute("DELETE FROM ImoState")
            cur.execute("DELETE FROM JigawaState")
            cur.execute("DELETE FROM KadunaState")
            cur.execute("DELETE FROM KanoState")
            cur.execute("DELETE FROM KastinaState")
            cur.execute("DELETE FROM KebbiState")
            cur.execute("DELETE FROM KogiState")
            cur.execute("DELETE FROM KwaraState")
            cur.execute("DELETE FROM LagosState")
            cur.execute("DELETE FROM NasarawaState")
            cur.execute("DELETE FROM NigerState")
            cur.execute("DELETE FROM OgunState")
            cur.execute("DELETE FROM OndoState")
            cur.execute("DELETE FROM OsunState")
            cur.execute("DELETE FROM OyoState")
            cur.execute("DELETE FROM PlateauState")
            cur.execute("DELETE FROM RiversState")
            cur.execute("DELETE FROM SokotoState")
            cur.execute("DELETE FROM TarabaState")
            cur.execute("DELETE FROM YobeState")
            cur.execute("DELETE FROM ZamfaraState")
        con.commit()
        msg = database + " Data Deleted"
        return render_template('admin.html', dbase=msg)


if __name__ == '__main__':
    app.run(debug=False)

