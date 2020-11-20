import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom';

const Sub = (props: {text: string}) => {
    const strings: string[] = props.text.split("\n");
    const nodes = strings.map((plain: string, i: number) => <p key={i}>{plain}</p>)
    return <div className="subtitles-single">{nodes}</div>
}

const Episode = () => {
    const { show, season, episode } = useParams<{show: string, season: string, episode: string}>();
    const [subs, setSubs] = useState<string[]>([])
    const subsNodes = subs.map((text: string, i: number) => <Sub key={i} text={text}/>);

    useEffect(() => {
        fetch(`/api/show/${show}/season/${season}/episode/${episode}`)
            .then(data => data.json())
            .then(data => setSubs(data.subs))
    }, [show, season, episode]);

    return (
        <div>
            {subsNodes}
        </div>
    )
}

export default Episode;