import React, { useEffect, useState } from 'react';
import { Link, useParams } from "react-router-dom";

interface Dictionary<T> {
    [key: string]: T;
}

interface IEpisode {
    episode: string,
    number: string | number,
    subtitle: string | null,
    image_url: string | null,
    available: boolean
};

interface IShow {
    title: string,
    season_titles_by_season: Dictionary<string>,
    episodes_by_season: Dictionary<IEpisode[]>
}

const Episode = (props: {episodeData: IEpisode, season: string, show: string}) => {
    return (
        <Link to={`/show/${props.show}/season/${props.season}/episode/${props.episodeData.number}`}>
            <h3>{props.episodeData.episode}</h3>
            <h5>{props.episodeData.subtitle}</h5>
            <img src={props.episodeData.image_url || ""} alt="Episode thumbnail" />
        </Link>
    )
}

const Season = (props: {episodes: IEpisode[], title: string, name: string, show: string}) => {
    const episodeNodes = props.episodes.map(
        (episodeData) => (
            <Episode episodeData={episodeData} show={props.show} season={props.name} />
        )
    );
    return (
        <div>
            <h3>{props.title}</h3>
            {episodeNodes}
        </div>
    );
};

const Show = () => {
    const { showSlug } = useParams<{ showSlug: string }>();

    const [show, setShow] = useState<IShow>({
        title: "loading",
        season_titles_by_season: {},
        episodes_by_season: {}
    });

    useEffect(() => {
        fetch(`/api/show/${showSlug}`)
            .then(data => data.json())
            .then(data => {
                setShow(data);
            });
    }, [showSlug])

    let seasons: JSX.Element[] = [];
    for (let [seasonName, episodes] of Object.entries(show.episodes_by_season)) {
        seasons.push(<Season
            show={showSlug}
            name={seasonName}
            title={show.season_titles_by_season[seasonName]}
            episodes={episodes} />
        );
    }

    return (
        <div>
            {seasons}
        </div>
    );
}

export default Show;