using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

#if UNITY_EDITOR
using UnityEditor;
#endif

public class MapRequestHandler {

  private static string requestDomain = Constants.APP_DOMAIN;

  public static IEnumerator getMap(GameSceneMain gameScene) {
  // TODO: create a common request handler class that all others extend, which has this set.
#if UNITY_EDITOR
    if (EditorApplication.isPlayingOrWillChangePlaymode) {
      requestDomain = Constants.LOCAL_HOST;
    }
#endif
    // TODO: Error check the PlayerState first.
    string query = "/map?player_id=" + PlayerState.GetPlayerKey();

    using(UnityWebRequest www = UnityWebRequest.Get(requestDomain + query)) {
      yield return www.SendWebRequest();

      if(www.isNetworkError) {
        // TODO: Make this show an error on the client, or something.
        Debug.LogError(www.error);
      } else {
        string rawjson = www.downloadHandler.text;
        ResponseModel response = JsonUtility.FromJson<ResponseModel>(rawjson);
        if (response.status == ResponseConstants.SUCCESS) {
          // We've gotten a successful response, deserialize the response into a model.
          GameModel gameModel = JsonUtility.FromJson<GameModel>(response.data);
          // Populate the GameState with the gameModel.
          GameState.UpdateGameModel(gameModel);
          // Tell the Map to update, now that the game state is updated.

          // Get a handle on the mapObject, and its script
          GameObject mapObject = GameObject.FindWithTag("Map");
          MapEngine mapEngine = mapObject.GetComponent(typeof(MapEngine)) as MapEngine;
          mapEngine.MarkMapAsOutOfDate();
        } else {
          // TODO: If getting the map doesn't work, expose the Error Message to the user.
          Debug.Log(response.status);
          Debug.Log(response.data);
          Debug.Log(response.error);
        }
      }
    }
  }
}
