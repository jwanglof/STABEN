-- phpMyAdmin SQL Dump
-- version 3.5.2.2
-- http://www.phpmyadmin.net
--
-- Värd: 127.0.0.1
-- Skapad: 02 aug 2013 kl 23:17
-- Serverversion: 5.5.27
-- PHP-version: 5.4.7

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Databas: `staben`
--

-- --------------------------------------------------------

--
-- Tabellstruktur `schedule`
--

CREATE TABLE IF NOT EXISTS `schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `week` int(11) DEFAULT NULL,
  `date` varchar(6) DEFAULT NULL,
  `weekday` varchar(10) DEFAULT NULL,
  `img_url` varchar(254) DEFAULT NULL,
  `time` varchar(20) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `href_div_id` varchar(4) DEFAULT NULL,
  `activity_info_day` varchar(1000) DEFAULT NULL,
  `activity_info_evening` varchar(800) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_schedule_date_date` (`date`),
  KEY `ix_schedule_date_week` (`week`),
  KEY `ix_schedule_date_activity_info_evening` (`activity_info_evening`(767)),
  KEY `ix_schedule_date_place` (`place`),
  KEY `ix_schedule_date_weekday` (`weekday`),
  KEY `ix_schedule_date_activity_info_day` (`activity_info_day`(767)),
  KEY `ix_schedule_date_href_div_id` (`href_div_id`),
  KEY `ix_schedule_date_img_url` (`img_url`),
  KEY `ix_schedule_date_time` (`time`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=22 ;

--
-- Dumpning av Data i tabell `schedule`
--

INSERT INTO `schedule` (`id`, `week`, `date`, `weekday`, `img_url`, `time`, `place`, `href_div_id`, `activity_info_day`, `activity_info_evening`) VALUES
(6, 1, '20/8', 'Tisdag', '1a_tisdag', '07:30 - 18:00', 'Folkets park, Campushallen, Campus Valla', '1a', 'Idag är det dags för <span class="nollanfont">minus</span> att besöka Folkets park kl. 07:30. Glöm inte nollebrickan, <span class="nollanfont">minus</span>! Här kommer <span class="nollanfont">minus</span> träffa fler  <span class="nollanfont">minus</span>, D-Group och andra faddrar. Dessa kommer att lära <span class="nollanfont">minus</span> att sjunga sin nollesång på yppersta och fagraste sätt. Därefter kommer <span class="nollanfont">minus</span> att skeppas vidare till Campushallen för att bli underhållna och träffa <span class="stabenfont">STABEN</span>. Superkuligt <span class="nollanfont">minus</span>! Det är dumt om <span class="nollanfont">minus</span> har sin cykel med sig, då <span class="nollanfont">minus</span> inte kommer att cykla. <span class="stabenfont">STABEN</span> rekommenderar därför att <span class="nollanfont">minus</span> lämnar sin cykel hemma. Det går bussar (linje 3, 12 och 13) till Gamla Linköping, ett ankarkast från Folkets Park.', 'Resten av dagen kommer <span class="nollanfont">minus</span> att bli uppropad, indelad, tilldelad, föreläst för och utfrågad. Uppropad för att universitetet ska se att <span class="nollanfont">minus</span> är där <span class="nollanfont">minus</span> bör vara, i Linkeboda, ju. Indelad och tilldelad för att <span class="nollanfont">minus</span> ska få en klass. Föreläst för att <span class="nollanfont">minus</span> ska lära sig saker och utfrågad för att <span class="nollanfont">minus</span> ska ha det roligt i nolle-p. <span class="nollanfont">minus</span> har en lång dag framför sig. <span class="nollanfont">minus</span> bör vara väl utvilad och dessutom ta med sig en frukt eller smörgås.'),
(7, 1, '21/8', 'Onsdag', '1b_onsdag', '08:00 - 01:00', 'Campus Valla, Viagraparken', '1b', 'Idag kommer <span class="nollanfont">minus</span> att få en nollegrupp och träffa sina toksnälla faddrar. Efter lunchen kommer <span class="nollanfont">minus</span> att lära sig hitta på universitetet. Typiskt dåligt för <span class="nollanfont">minus</span> att inte hitta! När <span class="nollanfont">minus</span> har lärt sig var man inte ska vara är det dags att bege sig till där <span class="nollanfont">minus</span> bör vara. Aristocats har då sin första av tre föreläsningar. I kursen TAEN33 Caps kommer Aristocats lära <span class="nollanfont">minus</span> konsten att capsa – att kasta prick med små runda objekt. Aristocats kommer att berätta allt <span class="nollanfont">minus</span> behöver veta, forskningen, reglerna och rekorden.', 'När <span class="nollanfont">minus</span> har lärt sig hur man capsar är det dags att testa sina nyvunna kunskaper i kursen. Detta sker genom del två: TAEN33 Caps – en praktisk laboration. Efter <span class="nollanfont">minus</span> är godkänd på laborationen kan <span class="nollanfont">minus</span> fortsätta det roliga i det ståtliga skeppet Kårallen. Där får <span class="nollanfont">minus</span> skaka på sina lurviga!'),
(8, 1, '22/8', 'Torsdag', '1c_torsdag', '08:00 - 21:00', 'Campus Valla, Linköping centrum, Fotbollsplan vid B-huset', '1c', 'Under lunchen kommer Lingsektionen att hålla sin lunchtävling Packling. Efter detta ska <span class="nollanfont">minus</span> lära sig att hitta i Linkeboda i <span class="stabenfont">STABEN</span>s tokskojsiga poängjakt. Här får <span class="nollanfont">minus</span> tillsammans med andra <span class="nollanfont">minus</span> hitta med karta i <span class="nollanfont">minus</span> nya hemstad. Sedan återkommer Aristocats med en till föreläsning. På denna får <span class="nollanfont">minus</span> lära sig allt om öl och häfv.', 'När <span class="nollanfont">minus</span> kan allt har <span class="nollanfont">minus</span> ett ypperligt tillfälle att testa det som <span class="nollanfont">minus</span> lärt sig. Praktiskt, <span class="nollanfont">minus</span>! När <span class="nollanfont">minus</span> känner sig färdigtestad kan <span class="nollanfont">minus</span> möta upp andra <span class="nollanfont">minus</span> för brännboll ju.'),
(9, 1, '23/8', 'Fredag', '1d_fredag', '08:00 - 01:00', 'Campus Valla, Hoben-parkeringen, Kårallen', '1d', 'Idag kommer <span class="nollanfont">minus</span> att fortsätta med skolandet. På lunchen är det dags för GF:s lunchtävling, G-Force. Där kan <span class="nollanfont">minus</span> se på när andra <span class="nollanfont">minus</span> skjuter vattenballonger på höga torn. Kanoners, <span class="nollanfont">minus</span>!', 'På kvällen är det dags för den sista av tre föreläsningar med de förträffliga Aristocats. Nu är det dags för <span class="nollanfont">minus</span> att lära sig hur man uppför sig och hur man inte uppför sig på en gasque. Efter föreläsningen är det dags för <span class="nollanfont">minus</span> att sätta sina nya kunskaper på prov på en riktig gasque. Efter gasqueandet kan <span class="nollanfont">minus</span> ännu en gång besöka sjömanskeppet Kårallen för att dansa loss.'),
(10, 1, '24/8', 'Lördag', '1e_lordag', '13:00 - 00:00', 'Campus Valla (samling), Svartåfors (hajk)', '1e', 'Äntligen sovmorgon <span class="nollanfont">minus</span>! Först kl 13.00 ska <span class="nollanfont">minus</span> träffas på campus för att sedan åka ut på äventyr. <span class="nollanfont">minus</span> ska vara mätta och glada, för det är nämligen dags för <span class="nollanfont">minus</span> att hajka! Nu får <span class="nollanfont">minus</span> inte glömma sin sovsäck, liggunderlag och cykel.', '<span class="stabenfont">STABEN</span> rekommenderar mörkrädda <span class="nollanfont">minus</span> att ta med sin absoluta favvosnuttefilt. <span class="stabenfont">STABEN</span> lovar att skydda <span class="nollanfont">minus</span> mot alla mörkrets monster och eventuella sjöodjur. Misströsta inte <span class="nollanfont">minus</span>, <span class="stabenfont">STABEN</span> ser allt och alla... alltid!'),
(11, 1, '25/8', 'Söndag', '1f_sondag', '08:00 - 12:00', 'Svartåfors, Hemma (?)', '1f', 'Upp och hoppa, <span class="nollanfont">minus</span>! Nu är det nämligen dags för D-sektionens excellenta styre att bjuda <span class="nollanfont">minus</span> på brunch. Efter denna utsökta måltid är det dags för <span class="nollanfont">minus</span> att bege sig hemåt tillsammans med sina supermysiga faddrar. Efter detta kan <span class="nollanfont">minus</span> göra vad <span class="nollanfont">minus</span> vill. Ringa mamma, kanske? Fixa lite mumsiga matlådor till veckan? Eller ha lite egentid med sin datormaskin?', '<span class="nollanfont">minus</span> gör det som behagar <span class="nollanfont">minus</span> mest!'),
(12, 2, '26/8', 'Måndag', '2a_mandag', '08:00 - 01:00', 'Campus Valla, [hg], Kårallen', '2a', 'Denna dag kommer <span class="nollanfont">minus</span> att vara utvilad från helgens hajk och redo för nya äventyr i skolbänken. På lunchen kommer <span class="nollanfont">minus</span> att titta på UrFadderiets lunchtävling.', 'På kvällen ska <span class="nollanfont">minus</span> få visa sina kunskaper i gasqueteknik på en supertrevlig sittning som överfaddrarna anordnar på [hg]. Här klär sig <span class="nollanfont">minus</span> bäst lite halvfint. Efter sittningen kan <span class="nollanfont">minus</span> ännu en gång skaka sina lurviga. Fast denna gång på det tokroliga och bästa nollediscot, <span class="stabenfont">STABEN</span> och GudFadderiets nolledisco ju!'),
(13, 2, '27/8', 'Tisdag', '2b_tisdag', '08:00 - 21:00', 'Campus Valla, hemma hos faddrar', '2b', 'Under lunchen är det äntligen dags för <span class="stabenfont">STABEN</span>s lunchtävling D-rift. Några tappra <span class="nollanfont">minus</span> kommer slänga sig ner för Märkesbacken i olika hemmameckade farkoster. Se till att vara där och heja på <span class="nollanfont">minus</span>, <span class="nollanfont">minus</span>.', 'På kvällen bjuder <span class="nollanfont">minus</span> supersnälla faddrar på mat. Om <span class="nollanfont">minus</span> inte är superduperduktig på att laga mat kan <span class="nollanfont">minus</span> kanske lära sig något om matlagningens ädla konst.'),
(14, 2, '28/8', 'Onsdag', '2c_onsdag', '08:00 - 01:00', 'Hoben-parkeringen', '2c', 'Gör dig redo <span class="nollanfont">minus</span>! Idag är det dags för den största festen under nolle-p, ju! München Hoben, förstås! Här kan <span class="nollanfont">minus</span> dricka öl ur löjligt stora sejdlar och lyssna på live-band! Här kommer <span class="nollanfont">minus</span> få träffa en massa trevligt folk!', 'Priset för detta kommer att vara cirka 80 kr.'),
(15, 2, '29/8', 'Torsdag', '2d_torsdag', '08:00 - 21:00', 'Campus Valla, Viagraparken', '2d', 'Idag får <span class="nollanfont">minus</span> för första gången träffa CQ på deras alldeles egna dag, CQs dag, <span class="nollanfont">minus</span>. Här kan <span class="nollanfont">minus</span> få gratis brunch på morgonsamlingen med kaffe/te som återställer <span class="nollanfont">minus</span> från gårdagens festligheter. Denna dag kommer <span class="nollanfont">minus</span> få träffa massor av gamla CQ fadderister som har jätteroliga kläder.', 'På kvällssidan kan <span class="nollanfont">minus</span> komma till Viagraparken för att leka med CQ, kanske höra ett eller annat gyckel och äta CQs speciella mat. Väldigt gott <span class="nollanfont">minus</span>!'),
(16, 2, '30/8', 'Fredag', '2e_fredag', '08:00 - 22:00', 'Campus Valla, grillplatser i Ryd, Skåland', '2e', 'På eftermiddagen kan <span class="nollanfont">minus</span> se när det tävlas i att dricka vätska på kortast tid, utan att spilla <span class="nollanfont">minus</span>! Det är Mpires häfv-tävling som går av stapeln. Efter denna tävling kan <span class="nollanfont">minus</span> se på när fadderierna skakar på sina lurviga. Då är det nämligen dags för megaYmpning!', 'På kvällen nalkas det grillning. <span class="nollanfont">minus</span> kommer att grilla med <span class="nollanfont">minus</span> klasskompisar, för att senare på kvällen träffa <span class="stabenfont">STABEN</span>. Vissa <span class="nollanfont">minus</span> skall då presentera sina nolleuppdrag. Kanontokskojsigt, ju!'),
(17, 2, '31/8', 'Lördag', '2f_lordag', '21:00 - 01:00', 'Campus Valla', '2f', 'Idag på kvällen kan <span class="nollanfont">minus</span> gå på SOF & Fortes utedisco, superduperkanonskojsigt ju!', ' '),
(18, 2, '1/9', 'Söndag', '2g_sondag', '00:00 - 00:00', 'Hemma (?)', '2g', 'Idag är <span class="nollanfont">minus</span> helt ledig, så <span class="nollanfont">minus</span> bör passa på att göra det <span class="nollanfont">minus</span> inte har hunnit göra.', 'Sova och tvätta kanske!'),
(19, 3, '2/9', 'Måndag', '3a_mandag', '12:00 - 13:00', 'Morgonsamlingsplatsen', '3a', 'Idag börjar läs-p, men var inte förtvivlad <span class="nollanfont">minus</span>. <span class="nollanfont">minus</span> kommer att få träffa <span class="stabenfont">STABEN</span> på lunchen. <span class="nollanfont">minus</span> kommer då få träffa <span class="stabenfont">STABEN</span>s <span class="stabenfont">STAB</span> och andra <span class="stabenfont">STABEN</span>s <span class="stabenfont">STAB</span>.', ' '),
(20, 3, '3/9', 'Tisdag', '3b_tisdag', '08:00 - 01:00', '[hg]', '3b', 'Idag kan <span class="nollanfont">minus</span> gå på en rolig kväll på Ryds herrgård, [hg]. Där kan <span class="nollanfont">minus</span> ha det tokskojsigt med andra <span class="nollanfont">minus</span> och där ska även vissa <span class="nollanfont">minus</span> redovisa sina nolleuppdrag.', 'Priset för detta kommer att vara cirka 75 kr.'),
(21, 3, '6/9', 'Fredag', '3c_fredag', '18:00 - 03:00', 'Colosseum, Kårallen', '3c', 'Idag ska <span class="nollanfont">minus</span> bli upphöjd till etta på <span class="nollanfont">minus</span> nollesittning, om <span class="nollanfont">minus</span> utfört sitt nolleuppdrag till <span class="stabenfont">STABEN</span>s belåtenhet. <span class="nollanfont">minus</span> ska först äta sig tokmätt på en trerättersmiddag, för att sedan gå på eftersläpp i Kårallen.', 'Sittningen kostar cirka 300 kr.');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
