function xFbConvSend(event_name, params) {
    const it = 'ACCOUNT_TOKEN_PLACEHOLDER'

    try {
        let fbc = null
        let fbp = null
        document.cookie.split(';').map(x => x.trim()).forEach((x) => {
            const parts = x.split('=')
            if (parts[0] == '_fbc')
                fbc = parts[1]
            if (parts[0] == '_fbp')
                fbp = parts[1]
        })
    
        const body = Object.assign({
            auth_token: it,
            event_name: event_name, 
            event_time: Math.floor(Number(new Date()) / 1000),
            fbc: fbc ? fbc : undefined,
            fbp: fbp ? fbp : undefined,
        }, params)
    
        fetch("https://fb-forwarder.ga/api/v1/fw/c", {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        }).then(x => console.log(x));
    } catch (e) {
        console.log(e)
    }
}
