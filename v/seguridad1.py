import os, shutil, subprocess, time
ROOT='/home/matiassosacom/public_html'
BK='/home/matiassosacom/backups-seguridad'
os.makedirs(BK,exist_ok=True); os.chmod(BK,0o700); os.system('chown matiassosacom:matiassosacom '+BK)
ts=time.strftime('%Y%m%d-%H%M%S')
log=[]
def test():
    r=subprocess.run(['curl','-sk','-o','/dev/null','-w','%{http_code}','-H','Host: www.matiassosa.com.ar','https://127.0.0.1/'],stdout=subprocess.PIPE)
    return r.stdout.decode()

# 1) .env: APP_DEBUG=false y permisos 640
env=ROOT+'/.env'
s=open(env).read()
shutil.copy(env,BK+'/env-'+ts); os.chmod(BK+'/env-'+ts,0o600)
if 'APP_DEBUG=true' in s:
    s=s.replace('APP_DEBUG=true','APP_DEBUG=false',1); open(env,'w').write(s); log.append('OK  APP_DEBUG=false')
else: log.append('YA  APP_DEBUG no era true')
os.chmod(env,0o640); os.system('chown matiassosacom:matiassosacom '+env); log.append('OK  .env 640')
os.system('cd %s && sudo -u matiassosacom php artisan config:clear >/dev/null 2>&1'%ROOT)

# 2) headers de seguridad + bloqueo de archivos ocultos/backups
ht=ROOT+'/.htaccess'
h=open(ht).read()
if 'ms-seguridad' in h: log.append('YA  .htaccess con headers')
else:
    shutil.copy(ht,BK+'/htaccess-'+ts)
    blk='''# ms-seguridad
<IfModule mod_headers.c>
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    Header always set Permissions-Policy "camera=(), microphone=(), payment=()"
    Header always set Strict-Transport-Security "max-age=31536000"
</IfModule>
<FilesMatch "^\\.(env|git|htpasswd|DS_Store)|\\.(sql|bak|old|log|zip|gz|tar)$|\\.antes-">
    <IfModule mod_authz_core.c>
        Require all denied
    </IfModule>
</FilesMatch>
# /ms-seguridad

'''
    open(ht,'w').write(blk+h)
    time.sleep(1)
    c=test()
    if c.startswith('5') or c=='000':
        shutil.copy(BK+'/htaccess-'+ts,ht); log.append('REVERTIDO .htaccess (HTTP %s)'%c)
    else: log.append('OK  headers en .htaccess (HTTP %s)'%c)
log.append('HTTP home: '+test())
print('\n'.join(log))
