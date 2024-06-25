import React, { useState, useEffect } from 'react';
import '../Demo.css'; // Подключение CSS файла
import CatImg from '../cat.jpg'; // Подключение изображения

const Demo = () => {
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(0);
  const [referralLink, setReferralLink] = useState('');

  // Получение реферальной ссылки
  useEffect(() => {
    const token = 'your-auth-token'; // Замените на ваш токен аутентификации
    fetch('http://127.0.0.1:8000/api/get_referral_link/', {
      headers: {
        'Authorization': `Bearer ${token}` // Убедитесь, что вы передаете токен аутентификации
      }
    })
    .then(response => response.json())
    .then(data => setReferralLink(data.referral_link))
    .catch(error => console.error('Error fetching referral link:', error));
  }, []);

  // Регистрация с реферальной ссылкой
  const registerWithReferral = (referralCode) => {
    const token = 'your-auth-token'; // Замените на ваш токен аутентификации
    fetch('http://127.0.0.1:8000/api/register_with_referral/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}` // Убедитесь, что вы передаете токен аутентификации
      },
      body: JSON.stringify({ referral_code: referralCode })
    })
    .then(response => response.json())
    .then(data => console.log('User registered with referral', data))
    .catch(error => console.error('Error registering with referral:', error));
  };

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
    }, 300);

    return () => {
      clearInterval(interval);
    };
  }, []);

  const value = 1; // Значение уровня
  const fillWidth = `${value * 50}%`;

  return (
    <div>
      {loading ? (
        <div className="game_page">
          <div className='game_view'>GeneCate's</div>
          <img className='cat_avatar' src={CatImg} alt="Cat Avatar"/>
          <div className="progress-bar">
            <div className="progress" style={{ width: `${progress}%` }}></div>
          </div>
        </div>
      ) : (
        <div className="game_page">
          <div className='welcome_view'>Welcome to GENECATE'S!</div>
          <div className='info_block'>
            Invite friends to receive early bird bonuses once the game is released. Early bird bonuses can only be obtained at this moment, while the game has not yet been released. Our team values those who are with us at this early stage
          </div>
          <img className='cat_avatar' src={CatImg} alt="Cat Avatar"/>
          <div className="progress-bar_lvl">
            <div className="progress" style={{ width: fillWidth }}>
              <span className="progress-text">Level {value}</span>
            </div>
          </div>
          <div className='lvl_info_block'>Number of invited friends: 1 out of 2 at level 2.</div>
          <div className='referal_block'>
            <div className='referal_info'>Referral link: {referralLink}</div>
            <button className='ref_button'>
              <svg role="img" xmlns="http://www.w3.org/2000/svg" width="48px" height="48px" viewBox="0 0 24 24" aria-labelledby="copyIconTitle" stroke="#0F5272" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" fill="none" color="#0F5272">
                <title id="copyIconTitle">Copy</title>
                <rect width="12" height="14" x="8" y="7"/>
                <polyline points="16 3 4 3 4 17"/>
              </svg>
            </button>
            <button className='invite_button' onClick={() => registerWithReferral('example-referral-code')}>Invite</button> {/* Замените 'example-referral-code' на нужный код */}
          </div>
          <div className='bonus_block'>Additional bonuses</div>
        </div>
      )}
    </div>
  );
}

export default Demo;
