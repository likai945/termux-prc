alias web='$HOME/.toolbox --web &'
alias gw='$HOME/.toolbox --gw'
alias laj='$HOME/jiankangji --laj'
alias lac='$HOME/jiankangji --lac'
alias laq='$HOME/jiankangji --laq'
alias lat='$HOME/jiankangji --lat'
alias lab='$HOME/jiankangji --lab'
alias jnj='$HOME/jiankangji --jnj'
alias jnh='$HOME/jiankangji --jnh'
alias jnq='$HOME/jiankangji --jnq'
alias jnt='$HOME/jiankangji --jnt'
alias jnb='$HOME/jiankangji --jnb'
alias jkj='$HOME/jiankangji'
alias ql='$HOME/.toolbox --ql'
alias hf='$HOME/.toolbox --hf'
alias gh='$HOME/.toolbox --github'
alias my='$HOME/.toolbox --gitee'
alias db='$HOME/.toolbox --db'
$HOME/.bird --ds
alias grep='grep --color'
alias ll='ls -l'
_day_=`date +%w`
[ $[_day_%6] -ne 0 ] && sshd
PS2='\[\e[0;32m\]>\[\e[0m\]'
alias diff='diff --color'
HISTTIMEFORMAT='%F %T '
shopt -s histappend
PROMPT_COMMAND="history -a"
GOPATH="/data/data/com.termux/files/home/grassland"
