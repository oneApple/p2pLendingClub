#########################################################################
# File Name: pack.sh
# Author: keyaming
# mail: keyamingcuc@gmail.com
# Created Time: 2013年05月14日 星期二 11时26分44秒
#########################################################################
#!/bin/bash
python pyinstaller.py  ~/github/p2plendingclud/p2pLendingClub/Main.py
cd Main/dist/Main
cp ~/github/p2plendingclud/p2pLendingClub/config.dat  ./
cp -r ~/github/p2plendingclud/p2pLendingClub/ico/  ./
cp -r ~/github/p2plendingclud/p2pLendingClub/DbRes/  ./


