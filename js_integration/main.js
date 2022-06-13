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
    
        const body = {
            auth_token: it,
            event_name: event_name, 
            event_time: Math.floor(Number(new Date()) / 1000),
            emails: params.emails || [],
            phones: params.phones || [],
            genders: params.genders || [],
            last_names: params.last_names || [],
            first_names: params.first_names || [],
            dates_of_birth: params.dates_of_birth || [],
            cities: params.cities || [],
            countries: params.countries || [],
            fbc: fbc ? fbc : undefined,
            fbp: fbp ? fbp : undefined
        }
    
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
