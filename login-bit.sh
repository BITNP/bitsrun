#!/usr/bin/bash
if [[ "$2" = "up" || "$2" = "connectivity-change" ]]; then
    curl -i http://t.cn 2>/dev/null | grep '10.0.0.55' >> /tmp/tmpvar
    if [ "$?" -eq 0 ]; then
        /usr/bin/bit-login login -v 
    fi
fi
