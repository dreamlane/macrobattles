using System.Collections.Generic;
using UnityEngine;

public class UnitScript : MonoBehaviour {
  public int x;
  public int y;

  private BottomBarResource bottomBarResource;
  private GameSceneMain gameSceneMain;

  void Start() {
    GameObject bottomBarObject = GameObject.FindWithTag("BottomBar");
    bottomBarResource = bottomBarObject.GetComponent(typeof(BottomBarResource))
        as BottomBarResource;

    GameObject mainCamera = GameObject.FindWithTag("MainCamera");
    gameSceneMain = mainCamera.GetComponent(typeof(GameSceneMain))
        as GameSceneMain;
    GameModel gameModel = gameSceneMain.GetGameModel();

  }

  void Update() {

  }

  void OnMouseUpAsButton() {
    Debug.Log("Clicked me a Unit: " + x + y);
    // Show x and y on client.
    if (bottomBarResource != null){
      
      bottomBarResource.tileCoordsText.text = "Unit x:" + x + " Unit y:" + y;
      bottomBarResource.resourceNameText.text = "Temp used to test unit click: ";

    }

   
  }

}
