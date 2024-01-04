create table sale (
  id int not null auto_increment,
  title text not null,
  category text,
  completed bool not null default FALSE,
  primary key(id)
);

SELECT * FROM todo ORDER BY length(title) desc;


