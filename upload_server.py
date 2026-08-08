#!/usr/bin/env python3
"""LAN file upload server — 手机传文件到电脑"""

import os, re, uuid, html
from http import server

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)
PORT = 8889

UPLOAD_HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>上传文件</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,sans-serif;background:#faf7f2;display:flex;align-items:center;justify-content:center;min-height:100vh;padding:20px}
.card{background:#fff;border-radius:16px;padding:40px;box-shadow:0 8px 32px rgba(0,0,0,0.08);text-align:center;width:100%;max-width:420px}
h1{font-size:1.4rem;margin-bottom:8px;color:#1a1a2e}
p{color:#6b6b7b;font-size:0.9rem;margin-bottom:24px}
.drop-zone{border:2px dashed #e8e4de;border-radius:12px;padding:40px 20px;cursor:pointer;transition:all 0.3s;margin-bottom:16px}
.drop-zone:hover,.drop-zone.dragover{border-color:#c77d61;background:#fdfaf7}
.drop-zone-icon{font-size:3rem;margin-bottom:12px}
.drop-zone-text{color:#6b6b7b;font-size:0.9rem}
input[type=file]{display:none}
#fileList{text-align:left;margin-top:16px}
#fileList li{font-size:0.85rem;color:#1a1a2e;padding:4px 0;list-style:none}
button{background:#c77d61;color:#fff;border:none;border-radius:8px;padding:12px 32px;font-size:1rem;cursor:pointer;transition:background 0.3s;width:100%}
button:hover{background:#b56a4e}
button:disabled{opacity:0.5;cursor:not-allowed}
.status{font-size:0.85rem;margin-top:12px;color:#6b6b7b}
.success{color:#4caf50}
.error{color:#e74c3c}
</style>
</head>
<body>
<div class="card">
<h1>上传文件到电脑</h1>
<p>选择或拖拽文件上传</p>
<div class="drop-zone" id="dropZone">
<div class="drop-zone-icon">&#128193;</div>
<div class="drop-zone-text">点击选择文件<br>或拖拽到此处</div>
</div>
<input type="file" id="fileInput" multiple>
<ul id="fileList"></ul>
<button id="uploadBtn" disabled>上传</button>
<div class="status" id="status"></div>
</div>
<script>
const dropZone=document.getElementById('dropZone');
const fileInput=document.getElementById('fileInput');
const fileList=document.getElementById('fileList');
const uploadBtn=document.getElementById('uploadBtn');
const status=document.getElementById('status');
let selectedFiles=[];
dropZone.addEventListener('click',()=>fileInput.click());
fileInput.addEventListener('change',(e)=>{selectFiles(e.target.files)});
dropZone.addEventListener('dragover',(e)=>{e.preventDefault();dropZone.classList.add('dragover')});
dropZone.addEventListener('dragleave',()=>{dropZone.classList.remove('dragover')});
dropZone.addEventListener('drop',(e)=>{e.preventDefault();dropZone.classList.remove('dragover');selectFiles(e.dataTransfer.files)});
function selectFiles(files){
  selectedFiles=Array.from(files);
  fileList.innerHTML='';
  selectedFiles.forEach(f=>{const li=document.createElement('li');li.textContent=f.name+' ('+(f.size/1024/1024).toFixed(1)+' MB)';fileList.appendChild(li)});
  uploadBtn.disabled=selectedFiles.length===0;
}
uploadBtn.addEventListener('click',async()=>{
  const formData=new FormData();
  selectedFiles.forEach(f=>formData.append('files',f));
  uploadBtn.disabled=true;status.textContent='上传中...';status.className='status';
  try{
    const res=await fetch('/upload',{method:'POST',body:formData});
    const text=await res.text();
    if(res.ok){status.textContent='上传成功! '+text;status.className='status success';fileList.innerHTML='';selectedFiles=[];}
    else{status.textContent='上传失败: '+text;status.className='status error';}
  }catch(e){status.textContent='上传失败: '+e.message;status.className='status error';}
  uploadBtn.disabled=false;
});
</script>
</body>
</html>'''


class UploadHandler(server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(UPLOAD_HTML.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path != '/upload':
            self.send_response(404)
            self.end_headers()
            return

        content_type = self.headers.get('Content-Type', '')
        if 'multipart/form-data' not in content_type:
            self.send_error(400, "需要 multipart/form-data")
            return

        boundary = re.search(r'boundary=(.+)', content_type)
        if not boundary:
            self.send_error(400, "缺少 boundary")
            return
        boundary = boundary.group(1).strip().strip('"')

        # Read raw body
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)

        # Parse multipart
        boundary_bytes = boundary.encode('utf-8')
        parts = body.split(b'--' + boundary_bytes)
        uploaded = []

        for part in parts:
            if not part.strip() or part.strip() == b'--':
                continue
            # Split headers and data
            header_end = part.find(b'\r\n\r\n')
            if header_end == -1:
                continue
            raw_headers = part[:header_end].decode('utf-8', errors='replace')
            file_data = part[header_end + 4:]
            file_data = file_data.rstrip(b'\r\n--')

            # Check if it's a file
            filename_match = re.search(r'filename="([^"]*)"', raw_headers)
            if not filename_match:
                continue

            filename = filename_match.group(1)
            if not filename:
                continue

            # Save file
            safe_name = os.path.basename(filename)
            path = os.path.join(UPLOAD_DIR, safe_name)
            base, ext = os.path.splitext(path)
            counter = 1
            while os.path.exists(path):
                path = f"{base}_{counter}{ext}"
                counter += 1
            with open(path, 'wb') as f:
                f.write(file_data)
            uploaded.append(os.path.basename(path))

        if uploaded:
            msg = f"已接收 {len(uploaded)} 个文件"
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(msg.encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("未收到文件".encode('utf-8'))


if __name__ == '__main__':
    with server.HTTPServer(("0.0.0.0", PORT), UploadHandler) as httpd:
        print(f"Upload server running at http://0.0.0.0:{PORT}")
        httpd.serve_forever()