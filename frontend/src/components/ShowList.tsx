import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { clearNavbar } from '../redux/actions/navbar';

interface IShowListItem { title: string, slug: string }

interface ISection { section: string, shows: IShowListItem[] }

interface Dictionary<T> {
  [key: string]: T;
}

const ShowListItem = (props: IShowListItem) => {
  const { slug, title } = props;
  return (
    <li>
      <Link to={`/show/${slug}`}>{title}</Link>
    </li>
  );
};

const Section = (props: ISection) => {
  const { section, shows } = props;
  return (
    <div className="episodes-section">
      <h3>{section}</h3>
      {shows.map((show) => <ShowListItem key={show.slug} slug={show.slug} title={show.title} />)}
    </div>
  );
};

const ShowList = () => {
  clearNavbar();
  const [shows, setShows] = useState<IShowListItem[]>([]);
  const sections: Dictionary<ISection> = {};

  useEffect(() => {
    fetch('/api/shows').then((data) => data.json()).then((data) => {
      setShows(data.shows);
    });
  }, []);

  shows.forEach((show: IShowListItem) => {
    const { slug } = show;
    const zeroethCharacter = slug.substr(0, 1).toUpperCase();
    if (!(zeroethCharacter in sections)) {
      sections[zeroethCharacter] = { section: zeroethCharacter, shows: [] };
    }

    sections[zeroethCharacter].shows.push(show);
  });

  const sectionList = Object.values(sections);

  return (
    <div>
      {sectionList.map((section) => (
        <Section
          key={section.section}
          section={section.section}
          shows={section.shows}
        />
      ))}
    </div>
  );
};

export default ShowList;
