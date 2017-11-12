using UnityEngine;

public class MapTileScript : MonoBehaviour {
  public int coordinate_x;
  public int coordinate_y;

  void Start() {

  }

  void Update() {
    // Check for a touch on the tile.
     if (Input.touchCount > 0) {
      // Get movement of the finger since last frame
      Debug.Log(Input.GetTouch(0).position);
    }
  }
}
