set PATH=C:\ProgramData\Anaconda3\;C:\ProgramData\Anaconda3\Scripts;c:\ProgramData\anaconda3\Library\bin;%PATH%
C:\ProgramData\Anaconda3\Scripts\conda config --set ssl_verify no
call C:\ProgramData\Anaconda3\Scripts\activate field3
cd C:\Users\pfleming\Desktop\git_tools\ghstats
git pull
python -u get_stats.py
