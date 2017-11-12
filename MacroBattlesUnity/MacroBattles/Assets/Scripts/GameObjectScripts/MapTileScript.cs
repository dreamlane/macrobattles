using UnityEngine;

public class MapTileScript : MonoBehaviour {
  public int x;
  public int y;

  void Start() {

  }

  void Update() {

  }

  void OnMouseUpAsButton() {
    Debug.Log("Clicked me: " + x + y);
  }
}
