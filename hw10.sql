-------------------------------------------------------------
                                                   -- DOGS --
-------------------------------------------------------------

create table parents as
  select "abraham" as parent, "barack" as child union
  select "abraham"          , "clinton"         union
  select "delano"           , "herbert"         union
  select "fillmore"         , "abraham"         union
  select "fillmore"         , "delano"          union
  select "fillmore"         , "grover"          union
  select "eisenhower"       , "fillmore";

create table dogs as
  select "abraham" as name, "long" as fur, 26 as height union
  select "barack"         , "short"      , 52           union
  select "clinton"        , "long"       , 47           union
  select "delano"         , "long"       , 46           union
  select "eisenhower"     , "short"      , 35           union
  select "fillmore"       , "curly"      , 32           union
  select "grover"         , "short"      , 28           union
  select "herbert"        , "curly"      , 31;

create table sizes as
  select "toy" as size, 24 as min, 28 as max union
  select "mini",        28,        35        union
  select "medium",      35,        45        union
  select "standard",    45,        60;

-------------------------------------------------------------
    -- PLEASE DO NOT CHANGE ANY DOG TABLES ABOVE THIS LINE --
-------------------------------------------------------------

-- The size of each dog
create table size_of_dogs as
    select name, size from dogs, sizes
    where height > min and height <= max;


-- All dogs with parents ordered by decreasing height of their parent
create table by_height as
   select child from parents, dogs where name = parent order by -height;

-- Sentences about siblings that are the same size
create table sentences as
    with
    siblings(first, second) as (
      select a.child, b.child from parents as a, parents as b
        where a.parent = b.parent and a.child < b.child
    )
  select first || " and " || second || " are " || a.size || " siblings"
    from siblings, size_of_dogs as a, size_of_dogs as b
    where a.size = b.size and a.name = first and b.name = second;
  

-- Heights and names of dogs that are above average in height among
-- dogs whose height has the same first digit.
create table above_average as
  with averages(digit, mean) as (
      select height/10, avg(height) from dogs group by height/10 having count(*)>1
  )
  select height, name from dogs, averages
         where height >= mean and digit = height/10;
        

-------------------------------------------------------------
                                     -- EUCLID CAFE TYCOON --
-------------------------------------------------------------

-- Locations of each cafe
create table cafes as
  select "nefeli" as name, 2 as location union
  select "brewed"        , 8             union
  select "hummingbird"   , 6;

-- Menu items at each cafe
create table menus as
  select "nefeli" as cafe, "espresso" as item union
  select "nefeli"        , "bagels"           union
  select "brewed"        , "coffee"           union
  select "brewed"        , "bagels"           union
  select "brewed"        , "muffins"          union
  select "hummingbird"   , "muffins"          union
  select "hummingbird"   , "eggs";

-- All locations on the block
create table locations as
  select 1 as n union
  select 2      union
  select 3      union
  select 4      union
  select 5      union
  select 6      union
  select 7      union
  select 8      union
  select 9      union
  select 10;

-------------------------------------------------------------
   -- PLEASE DO NOT CHANGE ANY CAFE TABLES ABOVE THIS LINE --
-------------------------------------------------------------

-- Locations without a cafe
create table open_locations as
  select n from locations, cafes group by n having min(abs(n-location)) > 0;


-- Items that could be placed on a menu at an open location
create table allowed as
  with item_locations(item, location) as (
    select item, location from cafes, menus where name = cafe
  )
    select n, item from locations, item_locations
      group by n, item having min(abs(n-location)) > 2;

