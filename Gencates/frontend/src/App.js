import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter as Router, Route,Routes, Switch } from 'react-router-dom';
import Phaser from 'phaser';
import './App.css';
import Loading from './asset/loading/loading.png';
import ForestMoggy from './asset/landing/forest_moggy_1.png';
import Info from './asset/landing/info.png';
import Lvl_1 from './asset/landing/lvl_1.png';
import Lvl_2 from './asset/landing/lvl_2.png';
import Lvl_3 from './asset/landing/lvl_3.png';
import Lvl_4 from './asset/landing/lvl_4.png';
import Lvl_5 from './asset/landing/lvl_5.png';
import Lvl_6 from './asset/landing/lvl_6.png';
import Lvl_7 from './asset/landing/lvl_7.png';
import Lvl_8 from './asset/landing/lvl_8.png';
import Lvl_8_bot from './asset/landing/lvl_8_bottom.png';
import Flask from './asset/welcome/Flask.png';
import Gems from './asset/welcome/Gems.png';
import Heart from './asset/welcome/Heart.png';
import Cancel from './asset/landing/Cancel.png'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/genecats" element={<Home />} />
        <Route path='/genecats/welcome' element={ <Welcome />} />
      </Routes>
    </Router>
  );
}
const Home = () => {
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [progress, setProgress] = useState(0);
  const value = 0; 
  const fillWidth = `${value * 50}%`;

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((oldProgress) => {
        if (oldProgress === 100) {
          clearInterval(interval);
          setLoading(false);
          return 100;
        }
        return Math.min(oldProgress + 10, 100);
      });
    }, 300); // Обновляем каждые 300 миллисекунд

    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <div>
      {loading ? (
        <div className="game_page">
          <div className='game_view'>GeneCats</div>
          <img className='cat_avatar' src={Loading}/>
          <div className="progress-bar">
            <div className="progress" style={{ width: `${progress}%` }}></div>
          </div>
          <div className='loading_view'>loading...</div>
        </div>
      ) : (
        <div className="game_page">
          {isModalOpen && (
        <div className="modal-backdrop">
          <div className="modal">
            <button className="modal-close" onClick={closeModal}>
              <img src={Cancel}/>
            </button>
            <div className="modal-content">
              <div className='modal_title'>The more friends You invite - the more coins and gifts You earn!</div>
              <div className='friend_content'>
                <div className='friend_block'>
                  <div className='friend_view'>1 fried</div>
                  <div className='friend_bonus'>
                    <div className='lawn_tile'>Lawn tile</div>
                    <div className='friend_coin'>1000 CatyCoins</div>
                  </div>
                </div>
                <div className='friend_block'>
                  <div className='friend_view'>2 fried</div>
                  <div className='friend_bonus'>
                    <div className='siamese'>Siamese cat</div>
                    <div className='friend_coin'>2500 CatyCoins</div>
                  </div>
                </div>
                <div className='friend_block'>
                  <div className='friend_view'>5 fried</div>
                  <div className='friend_bonus'>
                    <div className='maine_coon'>Maine Coon cat</div>
                    <div className='friend_coin'>5000 CatyCoins</div>
                  </div>
                </div>
                <div className='friend_block'>
                  <div className='friend_view'>10 fried</div>
                  <div className='friend_bonus'>
                    <div className='ragdoll'>Ragdoll cat</div>
                    <div className='amethyst'>Amethyst</div>
                    <div className='friend_coin'>10000 CatyCoins</div>
                  </div>
                </div>
                <div className='friend_block'>
                  <div className='friend_view'>25 fried</div>
                  <div className='friend_bonus'>
                    <div className='peterbald'>Peterbald cat</div>
                    <div className='amethyst'>5 amethysts</div>
                    <div className='friend_coin'>25000 CatyCoins</div>
                  </div>
                </div>
                <div className='friend_block'>
                  <div className='friend_view'>50 fried</div>
                  <div className='friend_bonus'>
                    <div className='serengeti'>Serengeti cat</div>
                    <div className='amethyst'>20 amethysts</div>
                    <div className='friend_coin'>50000 CatyCoins</div>
                  </div>
                </div>
                <div className='friend_block'>
                  <div className='friend_view'>100 fried</div>
                  <div className='friend_bonus'>
                    <div className='british'>British Shorhair cat</div>
                    <div className='amethyst'>50 amethysts</div>
                    <div className='friend_coin'>100000 CatyCoins</div>
                  </div>
                </div>
                <div className='friend_block'>
                  <div className='friend_view'>500 fried</div>
                  <div className='friend_bonus'>
                    <div className='bengal'>Bengal cat</div>
                    <div className='amethyst'>100 amethysts</div>
                    <div className='lawn_tile'>Lawn tile</div>
                    <div className='friend_coin'>500000 CatyCoins</div>
                  </div>
                </div>
                <div className='friend_block'>
                  <div className='friend_view'>2500 fried</div>
                  <div className='friend_bonus'>
                    <div className='sphynx'>Sphynx cat</div>
                    <div className='amethyst'>250 amethysts</div>
                    <div className='cat_house'>Cat's house</div>
                    <div className='friend_coin'>2500000 CatyCoins</div>
                  </div>
                </div>
                <div className='friend_block'>
                  <div className='friend_view'>10000 fried</div>
                  <div className='friend_bonus'>
                    <div className='khao'>Khao Manee cat</div>
                    <div className='lawn_tile'>Lawn tile</div>
                    <div className='cat_house'>Cat's house</div>
                    <div className='amethyst'>500 amethysts</div>
                    <div className='friend_coin'>10000000 CatyCoins</div>
                  </div>
                </div>
                
              </div>
            </div>
          </div>
        </div>
      )}
          <div className='landing_view'>GeneCats</div>
          <div className='info_block'>Invite friends to receive initial bonuses before the game is released. The initial bonus is available only to players who join before the project launches, as a token of appreciation for their support.</div>
          <div className='cat_lvl_container'>      
            <img className='cats_lvl' src={Lvl_8} />
          </div>
          <div className='progress_info_container'>
          <div className="progress-bar_lvl">
          <div className="progress" style={{ width: fillWidth }}>
          <span className="progress-text">Level {value}</span>
          </div>
        </div>
          <button className='info_button' onClick={openModal}><img src={Info}/></button>
          </div>
        <div className='lvl_info_block'>Invite 1 more friend for more gifts</div>
        <div className='referal_block'>
        <div className='referal_info'>GeneCats?start=Anus</div>
        <button className='ref_button'><svg role="img" xmlns="http://www.w3.org/2000/svg" width="26px" height="26px" viewBox="0 0 24 24" aria-labelledby="copyIconTitle" stroke="#fff" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none" color="#0F5272"> <title id="copyIconTitle">Copy</title> <rect width="12" height="14" x="8" y="7"/> <polyline points="16 3 4 3 4 17"/> </svg></button>
        <button className='invite_button'>Invite</button>
        </div>
        <img className='bot_gold' src={Lvl_8_bot}/>
        </div>
      )}
    </div>
  );
}

// <img className='cat_lvl' src={ForestMoggy} />
// <div className='cat_name'>Forest moggy Cat<br/>(Common)</div>

const Welcome = () => {
  const [isModalFlask, setIsModalFlask] = useState(false);
  const openFlask = () => setIsModalFlask(true);
  const closeFlask = () => setIsModalFlask(false);
  const [isModalJewelers, setIsModalJewelers] = useState(false);
  const openJewelers = () => setIsModalJewelers(true);
  const closeJewelers = () => setIsModalJewelers(false);
  const [isModalKnights, setIsModalKnights] = useState(false);
  const openKnights = () => setIsModalKnights(true);
  const closeKnights = () => setIsModalKnights(false);
  return(
    <div className="game_page">
      <div className='welcome_view'>Welcome<br/>to<br/>GeneCats</div>
      <div className='welcome_info'>Please, choose the fraction You want to join:</div>
      <div className='fraction'>
      <button onClick={openFlask} className='fraction_item'>
        <img className='fraction_icon_flask' src={Flask}/>
        <div className='fraction_text'>Alchemists</div>
      </button>
      {isModalFlask && (<div className="modal-backdrop_fraction">
          <div className="modal_fraction">
            <button className="modal-close" onClick={closeFlask}>
              <img src={Cancel}/>
            </button>
            <div className='modal_fraction_view'>Are You sure?</div>
            <img className='fraction_icon_flask' src={Flask}/>
            <div className='modal_fraction_buttons'>
              <button className='modal_fraction_button'>Yes</button>
              <button className='modal_fraction_button'>No</button>
            </div>
          </div>
      </div>)}
      <button onClick={openJewelers} className='fraction_item'>
        <img className='fraction_icon' src={Gems}/>
        <div className='fraction_text'>Jewelers</div>
      </button>
      {isModalJewelers && (<div className="modal-backdrop_fraction">
          <div className="modal_fraction">
            <button className="modal-close" onClick={closeJewelers}>
              <img src={Cancel}/>
            </button>
            <div className='modal_fraction_view'>Are You sure?</div>
            <img className='fraction_icon' src={Gems}/>
            <div className='modal_fraction_buttons'>
              <button className='modal_fraction_button'>Yes</button>
              <button className='modal_fraction_button'>No</button>
            </div>
          </div>
      </div>)}
      <button onClick={openKnights} className='fraction_item'>
        <img className='fraction_icon' src={Heart}/>
        <div className='fraction_text'>Knights</div>
      </button>
      {isModalKnights && (<div className="modal-backdrop_fraction">
          <div className="modal_fraction">
            <button className="modal-close" onClick={closeKnights}>
              <img src={Cancel}/>
            </button>
            <div className='modal_fraction_view'>Are You sure?</div>
            <img className='fraction_icon' src={Heart}/>
            <div className='modal_fraction_buttons'>
              <button className='modal_fraction_button'>Yes</button>
              <button className='modal_fraction_button'>No</button>
            </div>
          </div>
      </div>)}
      </div>
      <div className='welcome_info_2'>Caution! This choice is given once and forever</div>
    </div>
  )
}




export default App;
