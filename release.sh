#!/bin/bash
set -e

# Получаем версию из manifest.json
VERSION=$(jq -r .version custom_components/ha_integration_mobile_extra/manifest.json)
TAG="v$VERSION"

# Проверяем, есть ли уже такой тег
if git rev-parse "$TAG" >/dev/null 2>&1; then
  echo "Тег $TAG уже существует. Увеличьте версию в manifest.json."
  exit 1
fi

# Получаем предыдущий тег (если есть)
PREV_TAG=$(git tag --sort=-creatordate | head -n1)
if [ "$PREV_TAG" = "$TAG" ]; then
  PREV_TAG=$(git tag --sort=-creatordate | head -n2 | tail -n1)
fi

# Генерируем changelog
if [ -z "$PREV_TAG" ]; then
  CHANGELOG=$(git log --pretty=format:'* %s (%an)' )
else
  CHANGELOG=$(git log "$PREV_TAG"..HEAD --pretty=format:'* %s (%an)')
fi

# Создаём тег
 git tag "$TAG"
 git push origin "$TAG"

# Публикуем релиз на GitHub через gh
if [ -z "$CHANGELOG" ]; then
  CHANGELOG="Initial release."
fi

gh release create "$TAG" --title "$TAG" --notes "$CHANGELOG"

echo "Релиз $TAG опубликован!" 