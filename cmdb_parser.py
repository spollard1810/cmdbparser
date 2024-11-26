import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime

class CMDBParser:
    def __init__(self, root):
        self.root = root
        self.root.title("CMDB Parser")
        self.root.geometry("400x300")
        
        # Data storage
        self.cmdb_data = None
        self.hostname_data = None
        
        # Create GUI elements
        self.create_widgets()
    
    def create_widgets(self):
        # CMDB Load Button
        self.cmdb_btn = tk.Button(
            self.root, 
            text="Load CMDB CSV", 
            command=self.load_cmdb,
            width=20,
            height=2
        )
        self.cmdb_btn.pack(pady=20)
        
        # Hostname Load Button
        self.hostname_btn = tk.Button(
            self.root, 
            text="Load Hostname CSV", 
            command=self.load_hostnames,
            width=20,
            height=2
        )
        self.hostname_btn.pack(pady=20)
        
        # Parse Button
        self.parse_btn = tk.Button(
            self.root, 
            text="Parse and Save", 
            command=self.parse_data,
            width=20,
            height=2,
            state='disabled'
        )
        self.parse_btn.pack(pady=20)
        
        # Status Label
        self.status_label = tk.Label(self.root, text="Please load both CSV files")
        self.status_label.pack(pady=20)
    
    def load_cmdb(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                # Try UTF-8 first, then fallback to other encodings
                try:
                    self.cmdb_data = pd.read_csv(file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    self.cmdb_data = pd.read_csv(file_path, encoding='latin1')
                
                self.status_label.config(text="CMDB CSV loaded successfully")
                self.check_ready()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CMDB CSV: {str(e)}")
    
    def load_hostnames(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                # Try UTF-8 first, then fallback to other encodings
                try:
                    self.hostname_data = pd.read_csv(file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    self.hostname_data = pd.read_csv(file_path, encoding='latin1')
                
                # If there's only one column, assume it's the hostname
                if len(self.hostname_data.columns) == 1:
                    self.hostname_data.columns = ['hostname']
                elif 'hostname' not in self.hostname_data.columns:
                    # If multiple columns but no 'hostname', use first column
                    self.hostname_data = self.hostname_data.iloc[:, 0].to_frame()
                    self.hostname_data.columns = ['hostname']
                    
                self.status_label.config(text="Hostname CSV loaded successfully")
                self.check_ready()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load Hostname CSV: {str(e)}")
    
    def check_ready(self):
        if self.cmdb_data is not None and self.hostname_data is not None:
            self.parse_btn.config(state='normal')
            self.status_label.config(text="Ready to parse!")
    
    def parse_data(self):
        try:
            # Perform the matching and filtering
            result = pd.merge(
                self.hostname_data,
                self.cmdb_data,
                left_on='hostname',  # from input CSV
                right_on='name',     # from CMDB CSV
                how='left'
            )
            
            # Select only the three required columns
            columns = [
                'name',          # hostname from CMDB
                'ip_address',
                'model_id.name'
            ]
            result = result[columns]
            
            # Rename 'name' to 'hostname' for clarity
            result = result.rename(columns={'name': 'hostname'})
            
            # Remove rows where all values are NaN/empty
            result = result.dropna(how='all')
            
            # Generate output filename with date
            date_str = datetime.now().strftime("%Y-%m-%d")
            output_file = f"clean_csv_{date_str}.csv"
            
            # Save the result
            result.to_csv(output_file, index=False)
            messagebox.showinfo("Success", f"Data parsed and saved to {output_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse data: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CMDBParser(root)
    root.mainloop() 