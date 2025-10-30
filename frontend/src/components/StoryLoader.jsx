import { useState, useEffect } from 'react';
import { useParams, useNavigate } from "react-router-dom"
import axios from 'axios';
import LoadingStatus from "./LodingStatus.jsx"
import StoryGame from './StoryGame.jsx';


const API_BASE_URL = "/api"

function StoryLoader() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [story, setStory] = useState(null);
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null);

    const loadStory = async (storyId) => {
        setLoading(true)
        setError(null)

        try {
            const response = await axios.get('${API_BASE_URL}/stories/${storyId}/complete')
            setStory(response.data)
            setLoading(response.false)
        } catch (err) {
            if (err.response?.status === 404) {
                setError("Story is not found")
            } else {
                setError("Failde To Load Story")
            }
        } finally {
            setLoading(false)
        }


    }

    const createNewStory = async () => {
        navigate("/")
    }

    if (loading) {
        return <LoadingStatus theme={'story'} />
    }

    if (error) {
        return <div className="error-container">
            <div className='error-message'>
                <h2>Story Not Found</h2>
                <p>{error}</p>
                <button onClick={createNewStory}> Go to Story Generator </button>
            </div>
        </div>

    }

    if (story) {
        return <div className="story-loader">
            <StoryGame story={story} onNewStory={createNewStory} />

        </div>
    }

}

export default StoryLoader;