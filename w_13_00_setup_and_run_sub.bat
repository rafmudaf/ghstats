set PATH=C:\ProgramData\Anaconda3\;C:\ProgramData\Anaconda3\Scripts;%PATH%
C:\ProgramData\Anaconda3\Scripts\conda config --set ssl_verify no
call C:\ProgramData\Anaconda3\Scripts\activate field3
cd C:\Users\pfleming\Desktop\ghstats\ghstats
python -u get_stats.py
