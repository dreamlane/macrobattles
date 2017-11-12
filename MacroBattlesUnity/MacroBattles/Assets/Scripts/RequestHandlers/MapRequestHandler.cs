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
    using(UnityWebRequest www = UnityWebRequest.Get(requestDomain + "/map")) {
      yield return www.Send();

      if(www.isError) {
        // TODO: Make this show an error on the client, or something.
        Debug.Log(www.error);
      } else {
        string rawjson = www.downloadHandler.text;
        Debug.Log("Map GET request complete!");
        Debug.Log(www.downloadHandler.text);
        ResponseModel response = JsonUtility.FromJson<ResponseModel>(rawjson);
        if (response.status == ResponseConstants.SUCCESS) {
          // We've gotten a successful response, deserialize the response into a model.
          GameModel gameModel = JsonUtility.FromJson<GameModel>(response.data);

          // Hand the maptiles to the mapEngine.
          gameScene.SetGameModel(gameModel);
          Debug.Log(response.data);
        } else {
          Debug.Log(response.status);
          Debug.Log(response.data);
          Debug.Log(response.error);
        }
      }
    }
  }
}
