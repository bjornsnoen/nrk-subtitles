import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { ButtonType } from '../redux/actions/navbar';

export interface IEpisode {
  episode: string,
  number: string | number,
  season: string | number,
  subtitle: string | null,
  image_url: string | null,
  available: boolean
}

interface ISubsResponse {
  episode: IEpisode,
  previous_episode: IEpisode | null,
  next_episode: IEpisode | null,
  subs: string[]
}

const Sub = (props: { text: string }) => {
  const { text } = props;
  const strings = text.split('\n');
  const nodes = strings.map((plain: string) => <p>{plain}</p>);
  return <div className="subtitles-single">{nodes}</div>;
};

const episodeUrl = (episode: IEpisode, season: string | number, show: string) => {
  const { number: episodeNumber } = episode;
  return `/show/${show}/season/${season}/episode/${episodeNumber}`;
};

const Episode = () => {
  const { show, season, episode } = useParams<{ show: string, season: string, episode: string }>();
  const [subs, setSubs] = useState<string[]>([]);
  const subsNodes = subs.map((text: string) => <Sub text={text} />);
  const dispatch = useDispatch();

  useEffect(() => {
    fetch(`/api/show/${show}/season/${season}/episode/${episode}`)
      .then((data) => data.json())
      .then((data: ISubsResponse) => {
        const { subs: subtitles, previous_episode: previous, next_episode: next } = data;
        setSubs(subtitles);
        dispatch({
          type: 'navbar',
          buttonName: ButtonType.BACK,
          payload: previous ? episodeUrl(previous, previous.season, show) : null,
        });
        dispatch({
          type: 'navbar',
          buttonName: ButtonType.FORWARD,
          payload: next ? episodeUrl(next, next.season, show) : null,
        });
        dispatch({
          type: 'navbar',
          buttonName: ButtonType.UP,
          payload: `/show/${show}`,
        });
      });
  }, [show, season, episode]);

  window.scrollTo({ top: 0, behavior: 'smooth' });
  return (
    <div className="subtitles">
      {subsNodes}
    </div>
  );
};

export default Episode;
