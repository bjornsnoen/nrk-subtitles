import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

interface Dictionary<T> {
  [key: string]: T;
}

interface IEpisode {
  episode: string,
  number: string | number,
  subtitle: string | null,
  image_url: string | null,
  available: boolean
}

interface IShow {
  title: string,
  season_titles_by_season: Dictionary<string>,
  episodes_by_season: Dictionary<IEpisode[]>
}

const Episode = (props: { episodeData: IEpisode, season: string, show: string }) => {
  const { show, season, episodeData } = props;
  return (
    <Link to={`/show/${show}/season/${season}/episode/${episodeData.number}`}>
      <h3>{episodeData.episode}</h3>
      <h5>{episodeData.subtitle}</h5>
      <img src={episodeData.image_url || ''} alt="Episode thumbnail" />
    </Link>
  );
};

const Season = (props: { episodes: IEpisode[], title: string, name: string, show: string }) => {
  const {
    episodes, title, name, show,
  } = props;

  const episodeNodes = episodes.map(
    (episodeData) => (
      <Episode episodeData={episodeData} show={show} season={name} />
    ),
  );
  return (
    <div>
      <h3>{title}</h3>
      {episodeNodes}
    </div>
  );
};

const Show = () => {
  const { showSlug } = useParams<{ showSlug: string }>();

  const [show, setShow] = useState<IShow>({
    title: 'loading',
    season_titles_by_season: {},
    episodes_by_season: {},
  });

  useEffect(() => {
    fetch(`/api/show/${showSlug}`)
      .then((data) => data.json())
      .then((data) => {
        setShow(data);
      });
  }, [showSlug]);

  const seasons: JSX.Element[] = [];
  for (const [seasonName, episodes] of Object.entries(show.episodes_by_season)) {
    seasons.push(<Season
      show={showSlug}
      name={seasonName}
      title={show.season_titles_by_season[seasonName]}
      episodes={episodes}
    />);
  }

  return (
    <div>
      {seasons}
    </div>
  );
};

export default Show;
