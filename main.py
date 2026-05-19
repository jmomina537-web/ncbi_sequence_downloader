import ssl
import urllib.request
ssl._create_default_https_context = ssl._create_unverified_context

from Bio import Entrez, SeqIO
import csv
import os
import time

Entrez.email = "manoquaresh1587@gmail.com"

# Folders banao
os.makedirs("genbank", exist_ok=True)
os.makedirs("fasta", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# IDs read karo
with open("accession_ids.txt", "r") as file:
    accession_ids = [line.strip() for line in file if line.strip()]

print(f"Total IDs found: {len(accession_ids)}")
print(f"IDs: {accession_ids}\n")

# CSV setup
csv_file = "outputs/metadata.csv"
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Accession", "Name", "Organism", "Length", "Description"])

# Loop through all IDs
for i, accession in enumerate(accession_ids, 1):
    print(f"[{i}/{len(accession_ids)}] Processing: {accession}")
    
    try:
        # Data fetch karo
        with Entrez.efetch(
            db="nucleotide",
            id=accession,
            rettype="gb",
            retmode="text"
        ) as handle:
            data = handle.read()
        
        # GenBank file save karo
        with open(f"genbank/{accession}.gb", "w") as file:
            file.write(data)
        
        # Metadata nikal ke CSV me add karo
        record = SeqIO.read(f"genbank/{accession}.gb", "genbank")
        
        with open(csv_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                record.id,
                record.name,
                record.annotations.get('organism', 'N/A'),
                len(record.seq),
                record.description[:50]
            ])
        
        print(f"  ✅ Success: {record.annotations.get('organism', 'N/A')}, {len(record.seq)} bp")
        
        # NCBI ko rate limit se bachane ke liye 0.5 sec wait
        time.sleep(0.5)
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        continue

print(f"\n🎉 All Done! Check outputs/metadata.csv")
import ssl
import urllib.request
ssl._create_default_https_context = ssl._create_unverified_context

from Bio import Entrez, SeqIO
import csv
import os
import time

Entrez.email = "manoquaresh1587@gmail.com"

# Folders banao
os.makedirs("genbank", exist_ok=True)
os.makedirs("fasta", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# IDs read karo
with open("accession_ids.txt", "r") as file:
    accession_ids = [line.strip() for line in file if line.strip()]

print(f"Total IDs found: {len(accession_ids)}")
print(f"IDs: {accession_ids}\n")

# CSV setup
csv_file = "outputs/metadata.csv"
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Accession", "Name", "Organism", "Length", "Description"])

# Loop through all IDs
for i, accession in enumerate(accession_ids, 1):
    print(f"[{i}/{len(accession_ids)}] Processing: {accession}")
    
    try:
        # Data fetch karo
        with Entrez.efetch(
            db="nucleotide",
            id=accession,
            rettype="gb",
            retmode="text"
        ) as handle:
            data = handle.read()
        
        # GenBank file save karo
        with open(f"genbank/{accession}.gb", "w") as file:
            file.write(data)
        
        # Metadata nikal ke CSV me add karo
        record = SeqIO.read(f"genbank/{accession}.gb", "genbank")
        
        with open(csv_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                record.id,
                record.name,
                record.annotations.get('organism', 'N/A'),
                len(record.seq),
                record.description[:50]
            ])
        
        print(f"  ✅ Success: {record.annotations.get('organism', 'N/A')}, {len(record.seq)} bp")
        
        # NCBI ko rate limit se bachane ke liye 0.5 sec wait
        time.sleep(0.5)
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        continue

print(f"\n🎉 All Done! Check outputs/metadata.csv")

import matplotlib.pyplot as plt
import pandas as pd

# Step 23: FASTA conversion
print("\n--- Step 23: Converting to FASTA ---")

try:
    for gb_file in os.listdir("genbank"):
        if gb_file.endswith(".gb"):
            accession = gb_file.replace(".gb", "")
            
            record = SeqIO.read(f"genbank/{gb_file}", "genbank")
            
            # Check if sequence exists and is not too large
            if not record.seq:
                print(f"  ⚠️  Skipped {accession}: Sequence is empty")
                continue
            
            if len(record.seq) > 1000000:  # Skip if > 1 million bp
                print(f"  ⚠️  Skipped {accession}: Too large ({len(record.seq)} bp)")
                continue
            
            with open(f"fasta/{accession}.fasta", "w") as f:
                f.write(f">{record.id} {record.description}\n")
                f.write(str(record.seq) + "\n")
            
            print(f"  ✅ FASTA created: {accession}.fasta")
    
    print("FASTA conversion complete ✅")

except Exception as e:
    print(f"❌ FASTA Error: {e}")
    import pandas as pd
import os
from Bio import SeqIO

print("\nMerging all results into outputs folder...")

folder_path = "outputs"
all_data = []

for file in os.listdir(folder_path):
    if file.endswith(".fasta"):
        filepath = os.path.join(folder_path, file)
        try:
            record = SeqIO.read(filepath, "fasta")
            all_data.append({
                "Accession": record.id,
                "Description": record.description,
                "Length": len(record.seq),
                "File": file
            })
        except:
            pass

# outputs folder ke andar hi file banao
df = pd.DataFrame(all_data)
output_path = os.path.join(folder_path, "all_results.csv")
df.to_csv(output_path, index=False)

print(f"Done! {len(df)} records saved to outputs/all_results.csv")

import pandas as pd
import os
from Bio import SeqIO

print("\nMerging all results into outputs folder...")

folder_path = "genbank"  # yahan change kiya
all_data = []

for file in os.listdir(folder_path):
    if file.endswith(".gb"):  # yahan change kiya
        filepath = os.path.join(folder_path, file)
        try:
            record = SeqIO.read(filepath, "genbank")  # yahan bhi genbank likho
            all_data.append({
                "Accession": record.id,
                "Description": record.description,
                "Length": len(record.seq),
                "File": file
            })
        except:
            pass

df = pd.DataFrame(all_data)
output_path = os.path.join("outputs", "all_results.csv")
df.to_csv(output_path, index=False)

print(f"Done! {len(df)} records saved to outputs/all_results.csv")

import pandas as pd
import os
from Bio import SeqIO

print("\nMerging all results into outputs folder...")

folder_path = "genbank"  # yahan change kiya
all_data = []

for file in os.listdir(folder_path):
    if file.endswith(".gb"):  # yahan change kiya
        filepath = os.path.join(folder_path, file)
        try:
            record = SeqIO.read(filepath, "genbank")  # yahan bhi genbank likho
            all_data.append({
                "Accession": record.id,
                "Description": record.description,
                "Length": len(record.seq),
                "File": file
            })
        except:
            pass

df = pd.DataFrame(all_data)
output_path = os.path.join("outputs", "all_results.csv")
df.to_csv(output_path, index=False)

print(f"Done! {len(df)} records saved to outputs/all_results.csv")

import pandas as pd
import base64
from pathlib import Path
import datetime

def generate_html_report(csv_path="outputs/metadata.csv", plot_path="outputs/length_plot.png", output="report.html"):
    df = pd.read_csv(csv_path)
    
    # 1. Summary stats - tumhare CSV ke column names ke hisaab se
    total_seq = len(df)
    avg_len = df['Length'].mean() if 'Length' in df.columns else 0
    unique_org = df['Organism'].nunique() if 'Organism' in df.columns else 0
    total_files = df['Filename'].nunique() if 'Filename' in df.columns else total_seq
    
    # 2. Top 5 Organisms table
    if 'Organism' in df.columns:
        top_org_df = df['Organism'].value_counts().head(5).reset_index()
        top_org_df.columns = ['Organism', 'Count']
        top_org_html = top_org_df.to_html(index=False, classes="mini-table")
    else:
        top_org_html = "<p>No organism data</p>"
    
    # 3. Plot ko base64 mein convert karo
    plot_b64 = ""
    if Path(plot_path).exists():
        with open(plot_path, "rb") as f:
            plot_b64 = base64.b64encode(f.read()).decode()
    
    # 4. Main table - DataTables ke sath
    table_html = df.to_html(index=False, classes="display", table_id="seqTable", escape=False)
    
    # 5. HTML Template - Professional look
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NCBI Sequence Downloader - Final Report</title>
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f7f9; color: #333; padding: 30px; }}
            .container {{ max-width: 1400px; margin: 0 auto; }}
            h1 {{ color: #2c3e50; margin-bottom: 10px; border-left: 5px solid #3498db; padding-left: 15px; }}
            .subtitle {{ color: #7f8c8d; margin-bottom: 30px; }}
            
            .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px; }}
            .card {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.07); border-top: 4px solid #3498db; transition: transform 0.2s; }}
            .card:hover {{ transform: translateY(-5px); }}
            .card h2 {{ font-size: 40px; color: #3498db; margin-bottom: 5px; }}
            .card p {{ color: #95a5a6; font-weight: 600; text-transform: uppercase; font-size: 13px; letter-spacing: 1px; }}
            
            .section {{ background: white; padding: 30px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
            .section h3 {{ color: #2c3e50; margin-bottom: 20px; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }}
            
            .plot-container {{ text-align: center; }}
            .plot-container img {{ max-width: 100%; height: auto; border-radius: 8px; }}
            
            .download-btn {{ display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #3498db, #2980b9); color: white; text-decoration: none; border-radius: 8px; font-weight: bold; margin-bottom: 20px; transition: 0.3s; }}
            .download-btn:hover {{ transform: scale(1.05); box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4); }}
            
            .mini-table {{ width: 100%; border-collapse: collapse; }}
            .mini-table th {{ background: #3498db; color: white; padding: 12px; text-align: left; }}
            .mini-table td {{ padding: 10px; border-bottom: 1px solid #ecf0f1; }}
            .mini-table tr:hover {{ background: #f8f9fa; }}
            
            table.dataTable {{ width: 100% !important; }}
            .footer {{ text-align: center; margin-top: 40px; color: #95a5a6; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>NCBI Sequence Downloader - Metadata Report</h1>
            <p class="subtitle">Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <div class="summary-grid">
                <div class="card">
                    <h2>{total_seq}</h2>
                    <p>Total Sequences</p>
                </div>
                <div class="card">
                    <h2>{avg_len:.0f}</h2>
                    <p>Avg Length (bp)</p>
                </div>
                <div class="card">
                    <h2>{unique_org}</h2>
                    <p>Unique Organisms</p>
                </div>
                <div class="card">
                    <h2>{total_files}</h2>
                    <p>Files Processed</p>
                </div>
            </div>
            
            <div class="section">
                <h3>Top 5 Organisms</h3>
                {top_org_html}
            </div>
            
            {f'<div class="section"><h3>Sequence Length Distribution</h3><div class="plot-container"><img src="data:image/png;base64,{plot_b64}" alt="Length Distribution Plot"></div></div>' if plot_b64 else ''}
            
            <div class="section">
                <h3>Complete Metadata Table</h3>
                <a href="outputs/metadata.csv" class="download-btn" download>📥 Download CSV</a>
                {table_html}
            </div>
            
            <div class="footer">
                <p>NCBI Sequence Downloader Utility | Generated automatically</p>
            </div>
        </div>
        
        <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
        <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
        <script>
            $(document).ready(function() {{
                $('#seqTable').DataTable({{
                    "pageLength": 25,
                    "scrollX": true,
                    "order": [[4, "desc"]], // Length column se sort
                    "language": {{
                        "search": "Search sequences:"
                    }}
                }});
            }});
        </script>
    </body>
    </html>
    """
    
    with open(output, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print(f"✅ HTML Report successfully generated: {output}")
    print(f"📂 Open '{output}' in browser to view")

# Pipeline ke bilkul end mein ye line add karo
if __name__ == "__main__":
    # ...tumhara existing code...
    generate_html_report()
    import os
import pandas as pd
import base64
import matplotlib.pyplot as plt
from pathlib import Path
import datetime
import time

# ========== 1. HTML REPORT FUNCTION ==========
def generate_html_report(csv_path="outputs/metadata.csv", output="report.html"):
    print("\n📊 Generating HTML Report...")
    
    if not Path(csv_path).exists():
        print(f"❌ Error: {csv_path} not found! Pehle metadata.csv banao.")
        return
    
    df = pd.read_csv(csv_path)
    print(f"Columns found: {list(df.columns)}")
    print(f"Total rows: {len(df)}")
    
    # Column names auto-detect - capital ho ya small
    len_col = 'Length' if 'Length' in df.columns else 'length'
    org_col = 'Organism' if 'Organism' in df.columns else 'organism'
    acc_col = 'Accession' if 'Accession' in df.columns else 'accession'
    
    # 1. Summary stats
    total_seq = len(df)
    avg_len = df[len_col].mean() if len_col in df.columns else 0
    unique_org = df[org_col].nunique() if org_col in df.columns else 0
    
    # 2. Length plot banao agar nahi hai
    plot_path = "outputs/length_plot.png"
    Path("outputs").mkdir(exist_ok=True)
    plt.figure(figsize=(10,6))
    df[len_col].hist(bins=30, color='#3498db', edgecolor='black')
    plt.title('Sequence Length Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Length (bp)')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()
    
    # 3. Plot ko base64
    with open(plot_path, "rb") as f:
        plot_b64 = base64.b64encode(f.read()).decode()
    
    # 4. Top 5 Organisms
    top_org = df[org_col].value_counts().head(5).reset_index() if org_col in df.columns else pd.DataFrame()
    if not top_org.empty:
        top_org.columns = ['Organism', 'Count']
        org_html = top_org.to_html(index=False, classes="mini-table")
    else:
        org_html = "<p>No organism data</p>"
    
    # 5. Main table
    table_html = df.to_html(index=False, classes="display", table_id="seqTable", escape=False)
    
    # 6. HTML Template
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NCBI Sequence Downloader Report</title>
        <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Arial; background: #f4f7f9; padding: 30px; }}
            h1 {{ color: #2c3e50; border-left: 5px solid #3498db; padding-left: 15px; margin-bottom: 10px; }}
            .subtitle {{ color: #7f8c8d; margin-bottom: 30px; }}
            .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
            .card {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.07); text-align: center; border-top: 4px solid #3498db; }}
            .card h2 {{ font-size: 38px; color: #3498db; margin: 0; }}
            .card p {{ color: #7f8c8d; font-weight: 600; margin-top: 8px; text-transform: uppercase; font-size: 13px; }}
            .section {{ background: white; padding: 30px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
            .section h3 {{ color: #2c3e50; margin-bottom: 20px; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }}
            .plot img {{ max-width: 100%; height: auto; border-radius: 8px; }}
            .download-btn {{ display: inline-block; padding: 12px 25px; background: #3498db; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; margin-right: 10px; margin-bottom: 15px; }}
            .download-btn:hover {{ background: #2980b9; }}
            .mini-table {{ width: 50%; border-collapse: collapse; }}
            .mini-table th {{ background: #3498db; color: white; padding: 12px; text-align: left; }}
            .mini-table td {{ padding: 10px; border-bottom: 1px solid #ecf0f1; }}
            table.dataTable {{ width: 100% !important; }}
        </style>
    </head>
    <body>
        <h1>NCBI Sequence Downloader - Metadata Report</h1>
        <p class="subtitle">Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary">
            <div class="card"><h2>{total_seq}</h2><p>Total Sequences</p></div>
            <div class="card"><h2>{avg_len:.0f}</h2><p>Avg Length (bp)</p></div>
            <div class="card"><h2>{unique_org}</h2><p>Unique Organisms</p></div>
            <div class="card"><h2>{total_seq}</h2><p>Files Processed</p></div>
        </div>
        
        <div class="section">
            <h3>Top 5 Organisms</h3>
            {org_html}
        </div>
        
        <div class="section">
            <h3>Sequence Length Distribution</h3>
            <div class="plot"><img src="data:image/png;base64,{plot_b64}"></div>
        </div>
        
        <div class="section">
            <h3>Complete Metadata Table</h3>
            <a href="outputs/metadata.csv" class="download-btn" download>📥 Download CSV</a>
            {table_html}
        </div>
        
        <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
        <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
        <script>
            $(document).ready(function() {{
                $('#seqTable').DataTable({{
                    "pageLength": 25,
                    "scrollX": true,
                    "order": [[4, "desc"]]
                }});
            }});
        </script>
    </body>
    </html>
    """
    
    with open(output, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print(f"✅ HTML Report successfully generated: {output}")
    print(f"📂 Open '{output}' in browser to view")

# ========== 2. MAIN FUNCTION ==========
def main():
    print("NCBI Sequence Downloader Pipeline")
    print("="*50)
    
    # YAHAN TUMHARA EXISTING PIPELINE CODE HAI
    # Download, FASTA conversion, metadata.csv creation wala code
    # Agar metadata.csv already bani hui hai to ye function sirf report banayega
    
    # Example: Sirf report test karne ke liye
    time.sleep(1)
    print("Pipeline steps complete...")

# ========== 3. EXECUTION ==========
if __name__ == "__main__":
    main()  # 1. Pehle pipeline
    generate_html_report()  # 2. Phir HTML report
    def main():
    print("NCBI Sequence Downloader Pipeline")
    print("="*50)

    # YE 2 LINE ADD KAR DO - SKIP DOWNLOAD
    print("Skipping download... metadata.csv already exists")
    return # <-- is se function yahin khatam ho jayega

    # baqi purana download wala code neeche rahega, chalega hi nahi
```[Best]

Phir `python main.py` run karo. Sirf 2 sec mein report ban jayegi.

#### **Tareeqa 2: Alag Command Banao**
Terminal mein ye likho:
```bash
python -c "from main import generate_html_report; generate_html_report()"