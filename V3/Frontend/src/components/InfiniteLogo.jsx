import img1 from '../Assets/LOGO_CAROUSEL/BeautifulSoup.jpg';
import img2 from '../Assets/LOGO_CAROUSEL/Bootstrap.jpg';
import img3 from '../Assets/LOGO_CAROUSEL/FastAPI.jpg';
import img4 from '../Assets/LOGO_CAROUSEL/Graphviz.jpg';
import img5 from '../Assets/LOGO_CAROUSEL/NetworkX.jpg';
import img6 from '../Assets/LOGO_CAROUSEL/pandas.jpg';
import img7 from '../Assets/LOGO_CAROUSEL/pyTiger.jpg';
import img8 from '../Assets/LOGO_CAROUSEL/React.jpg';
import img9 from '../Assets/LOGO_CAROUSEL/Requests.jpg';
import img10 from '../Assets/LOGO_CAROUSEL/YAML.jpg';



const InfiniteLogo = () => {
  return (
    <>
      <style>
        {`
          * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
          }

          
          @keyframes slide {
            from {
              transform: translateX(0);
            }
            to {
              transform: translateX(-100%);
            }
          }

          .logos {
            overflow: hidden;
            padding: 60px 0;
            
            white-space: nowrap;
            position: relative;
          }

          .logos:before,
          .logos:after {
            position: absolute;
            top: 0;
            width: 250px;
            height: 100%;
            content: '';
            z-index: 2;
          }

          .logos:before {
            left: 0;
            background: linear-gradient(to left, rgba(255, 255, 255, 0), white);
          }

          .logos:after {
            right: 0;
            background: linear-gradient(to right, rgba(255, 255, 255, 0), white);
          }

          .logos:hover .logos-slide {
            animation-play-state: paused;
          }

          .logos-slide {
            display: inline-block;
            animation: 35s slide infinite linear;
          }

          .logos-slide img {
            height: 50px;
            margin: 0 40px;
          }
        `}
      </style>
      <div className="logos">
        <div className="logos-slide">
         <img src={img1} alt="Logo" />
         <img src={img2} alt="Logo" />
         <img src={img3} alt="Logo" />
         <img src={img4} alt="Logo" />
         <img src={img5} alt="Logo" />
         <img src={img6} alt="Logo" />
         <img src={img7} alt="Logo" />
         <img src={img8} alt="Logo" />
         <img src={img9} alt="Logo" />
         <img src={img10} alt="Logo" />
        </div>
        <div className="logos-slide">
        <img src={img1} alt="Logo" />
         <img src={img2} alt="Logo" />
         <img src={img3} alt="Logo" />
         <img src={img4} alt="Logo" />
         <img src={img5} alt="Logo" />
         <img src={img6} alt="Logo" />
         <img src={img7} alt="Logo" />
         <img src={img8} alt="Logo" />
         <img src={img9} alt="Logo" />
         <img src={img10} alt="Logo" />
        </div>
      </div>
    </>
  );
};

export default InfiniteLogo;