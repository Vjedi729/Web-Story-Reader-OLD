create table Users(
	username varchar(30) primary key,
	email varchar(100),
	password varchar(100),
	sign_up_date date,
	links_to_other_site_account varchar(200)
	);
	
create table Stories(
	story_id int primary key,
	username varchar(30),
	summary varchar(200),
	maturity_rating decimal(10,2),
	genreA varchar(100),
	genreB varchar(100),
	language varchar(30),
	last_update_time datetime,
	inital_update_time datetime,
	word_count bigint,
	completion_status int,
	foreign key (username) references Users(username)
	);
	
create table Fanfic_User(
	fanfic_username varchar(30) primary key,
	local_username varchar(30),
	foreign key (local_username) references Users(username)
	);
	
create table AO3_User(
	AO3_username varchar(30) primary key,
	local_username varchar(30),
	foreign key (local_username) references Users(username)
	);
	
create table FicPress_user(
	FicPress_username varchar(30) primary key,
	local_username varchar(30),
	foreign key (local_username) references Users(username)
	);
	
create table friends(
	username1 varchar(30),
	username2 varchar(30),
	primary key (username1,username2),
	foreign key (username1) references Users(username),
	foreign key (username2) references Users(username)
	);
	
create table Readers_read_records(
	record_id int primary key,
	review int,
	rating decimal(10,2),
	original_time_stamp timestamp,
	latest_time_stame timestamp,
	username varchar(30),
	foreign key (username) references Users(username)
	);
	
create table Contain_Chapters(
	story_id int, 
	chapter_num int , 
	upload_time datetime, 
	word_count bigint,
	primary key (story_id, chapter_num),
	foreign key (story_id) references Stories(story_id)
	);
	
create table Contain_Characters(
	story_id int,
	character varchar(200),
	primary key(story_id,character),
	foreign key (story_id) references Stories(story_id)
	);
	
create table Contain_romantic_pairings(
	story_id int,
	romantic_pairing varchar(200),
	primary key (story_id, romantic_pairing),
	foreign key (story_id) references Stories(story_id)	
	);
	
create table read_up_to(
	story_id int,
	chapter_num int,
	record_id int,
	primary key(story_id, chapter_num, record_id),
	foreign key (story_id, chapter_num) references Contain_Chapters(story_id, chapter_num),
	foreign key (record_id) references Readers_read_records(record_id)	

	);