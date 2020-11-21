import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const Sub = (props: {text: string}) => {
  const { text } = props;
  const strings = text.split('\n');
  const nodes = strings.map((plain: string) => <p>{plain}</p>);
  return <div className="subtitles-single">{nodes}</div>;
};

const Episode = () => {
  const { show, season, episode } = useParams<{show: string, season: string, episode: string}>();
  const [subs, setSubs] = useState<string[]>([]);
  const subsNodes = subs.map((text: string) => <Sub text={text} />);

  useEffect(() => {
    fetch(`/api/show/${show}/season/${season}/episode/${episode}`)
      .then((data) => data.json())
      .then((data) => setSubs(data.subs));
  }, [show, season, episode]);

  return (
    <div>
      {subsNodes}
    </div>
  );
};

export default Episode;
