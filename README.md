# MultimediaProject
### Unreal Engine Tool for Video Stabilization and Artifact Removal

This Unreal Engine tool focuses on video stabilization and artifact removal, allowing users to enhance the quality of their videos by eliminating unwanted movements and visual artifacts. The tool aims to make projects look more polished and professional.

**Features:**

1. **Video Stabilization:**
   - **Motion Estimation Algorithm:** Utilizes Optical Flow (Lucas-Kanade) to estimate camera movement between frames.
   - **Motion Correction Algorithm:** Implements a simple smoothing technique, such as Motion Vector Integration.
   - **Granular Control:** Offers a simple slider to adjust stabilization intensity.

2. **Artifact Removal:**
   - **Noise Reduction:** Implements a median filter to reduce noise.
   - **Adjustable Parameters:** A single slider to adjust the intensity of the noise reduction filter.

3. **User Interface:**
   - **Intuitive Layout:** Creates a simple user interface with buttons to load the video, apply stabilization, and remove artifacts.
   - **Real-Time Preview System:** Integrates a preview feature to immediately show the effect of stabilization and noise reduction.
   - **Saving Options:** Adds a button to save the enhanced video in a common format (e.g., MP4).
