function xFbConvSend(click_id, params) {
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
            event_time: Math.floor(Number(new Date()) / 1000),
            fbc: fbc ? fbc : undefined,
            fbp: fbp ? fbp : undefined,
        }, params)

        let xhr = new XMLHttpRequest()
        xhr.open('POST', `https://conversion-router.tech/api/v1/fw/c/${click_id}`, false)
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify(body))
    } catch (e) {
        console.log(e)
    }
}


