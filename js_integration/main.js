function xFbConvSend(event_name, emails=[], phones=[], genders=[], last_names=[], first_names=[], cities=[], countries=[], dates_of_birth=[]) {
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
            emails: emails,
            phones: phones,
            genders: genders,
            last_names: last_names,
            first_names: first_names,
            dates_of_birth: dates_of_birth,
            cities: cities,
            countries: countries,
            fbc: undefined,
            fbp: undefined
        }
        if (fbc) body.fbc = fbc
        if (fbp) body.fbp = fbp
    
        fetch("http://localhost:8092/api/v1/fw/c", {
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