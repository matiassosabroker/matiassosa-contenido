import subprocess
V='/home/matiassosacom/public_html/resources/views'
def sh(c): print(subprocess.run(c,shell=True,capture_output=True,text=True).stdout)
sh("cd %s && grep -rn '<h1' --include=*.blade.php . | cut -c1-170"%V)
sh("cd %s && grep -rn 'user-scalable' . | cut -c1-120"%V)
sh("cd %s && grep -rln 'instagram.com' . "%V)
sh("cd %s && ls front/pages | tr '\\n' ' '"%V)
