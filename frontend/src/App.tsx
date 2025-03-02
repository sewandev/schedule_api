import './App.css'
import Form from './assets/scripts/form.tsx';

function App() {

  return (
    <>    
      <div className='api'>
          <div className='left-panel-container'>
            <div className='left-panel'>
              <div className='api-logo'>
              <i className="fa-solid fa-dog"></i>Test.api
              </div>
              <div className='container'>
                  <a href=""><li>
                    <i className="fa-regular fa-clock"></i> Availability
                  </li></a>
                  <a href=""><li>
                    <i className="fa-regular fa-calendar"></i> Dates
                  </li></a>
                  <a href=""><li>
                    <i className="fa-regular fa-bell"></i> Notification
                  </li></a>
              </div>
              <div className='bottom-container'>
                    <a href=""><li>
                    <i className="fa-regular fa-circle-question"></i> Help
                    </li></a>
              </div>
            </div>
            </div>
            <div className="calendary">
                    <div>
                        <Form />
                    </div>     
            </div>
            <div className='right-panel'>
              <div className='panel'>
                <div className='user'>
                    <div className='user-img'>
                      <img src="src/assets/img/Oliva_profile.webp" alt="" />
                    </div>
                  <div className='info'>
                    <div className='name'>
                      <h1>Bicuit Oliva D.</h1>
                    </div>
                    <div className='loc'>
                      <h3>Valparaíso, <strong>San Felipe</strong></h3>
                    </div>
                  </div>
                </div>
                <div className='container'>
                  <div className='text'>
                    <p>Account Settings</p>
                  </div>
                    <a href=""><li>
                      <i className="fa-regular fa-circle-user"></i> Profile
                    </li></a>
                    <a href=""><li>
                      <i className="fa-solid fa-link"></i> About me
                    </li></a>
                    <a href=""><li>
                     <i className="fa-solid fa-ellipsis-vertical"></i> All Setting
                    </li></a>
                </div>
                <div className='resource-container'>
                  <div className='text'>
                    <p>Resources</p>
                  </div>
                    <a href=""><li>
                      <i className="fa-regular fa-circle-user"></i> About Us
                    </li></a>
                    <a href=""><li>
                      <i className="fa-solid fa-arrow-up-right-from-square"></i> mawanstudio.com
                    </li></a>
                    <a href=""><li>
                      <i className="fa-solid fa-arrow-right-from-bracket"></i> Logout
                    </li></a>
                </div>
              </div>
            </div>
        </div>
      </>
  )
}

export default App
