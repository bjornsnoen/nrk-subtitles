import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { clearNavbar } from '../redux/actions/navbar';

interface IShowListItem { title: string, slug: string }

const ShowListItem = (props: IShowListItem) => {
  const { slug, title } = props;
  return (
    <li>
      <Link to={`/show/${slug}`}>{title}</Link>
    </li>
  );
};

const ShowList = () => {
  const [shows, setShows] = useState<IShowListItem[]>([]);
  clearNavbar();

  useEffect(() => {
    fetch('/api/shows').then((data) => data.json()).then((data) => {
      setShows(data.shows);
    });
  }, []);

  return (
    <ul>
      {shows.map((showData) => (
        <ShowListItem
          key={showData.slug}
          title={showData.title}
          slug={showData.slug}
        />
      ))}
    </ul>
  );
};

export default ShowList;
